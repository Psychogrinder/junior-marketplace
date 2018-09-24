from trello import TrelloClient, ResourceUnavailable, Unauthorized, WebHook
from contextlib import contextmanager
import re
from flask import url_for
import requests
from marketplace.models import Producer, Product, Order
from marketplace import app, db, celery


@contextmanager
def authenticated(token):
    client = TrelloClient(api_key=app.config['TRELLO_API_KEY'], token=token)
    try:
        yield client
    except (ResourceUnavailable, Unauthorized):
        pass


@celery.task
def commit_change(board_id, trello_token, producer_id):
    producer = Producer.query.get(producer_id)
    producer.link_trello_account(trello_token, board_id)
    db.session.commit()


@celery.task
def create_new_board(name, token):
    with authenticated(token) as client:
        new_board = client.add_board(name, default_lists=False)
        for index, list_name in enumerate(app.config['TRELLO_BOARD_LISTS'], 1):
            new_board.add_list(list_name, pos=index)
        return new_board.id


def _find_list(name, board_id, client):
    board = client.get_board(board_id)
    all_lists = board.all_lists()
    for _list in all_lists:
        if _list.name.lower() == name.lower():
            return _list
    return all_lists[0]


@celery.task
def create_card_if_producer_linked_trello_account(producer_id, order_id, webhook=True):
    producer = Producer.query.get(producer_id)
    order = Order.query.get(order_id)
    if producer is None or producer.trello_token is None:
        return
    with authenticated(producer.trello_token) as client:
        board = client.get_board(producer.trello_board_id)
        list_new = board.all_lists()[0]
        _add_card(order, list_new, client)
        if webhook:
            callback_url = 'https://xtramarket.ru' + url_for('trellowebhook', _external=False)
            hook = _create_webhook(callback_url, board.id, client)


def _create_webhook(callback_url, id_model, client):
    url = "https://api.trello.com/1/webhooks/"
    data = {'callbackURL': callback_url, 'idModel': id_model, 'description': None}
    response = requests.post(url, data=data, auth=client.oauth)
    if response.status_code == 200:
        hook_id = response.json()['id']
        return WebHook(client, client.resource_owner_key, hook_id, None, id_model, callback_url, True)
    else:
        return False


def _create_card_template(order):
    products = []
    for product_id, quantity in order.order_items_json.items():
        product = Product.query.get(product_id)
        products.append(f'> **Продукт**: {product.name}\n> **Артикул**: {product.id}\n> **Количество**: {quantity}\n')
    desc = f'\n```\nДоставка:  {order.delivery_method}\nПокупатель: {order.first_name} {order.last_name}\nАдрес: {order.delivery_address}\nТелефон: {order.consumer_phone}\nПочта: {order.consumer_email}\n```\n'
    return '\n---\n'.join(products) + desc



def _add_card(order, _list, client):
    name = f'Заказ №{order.id}'
    description = _create_card_template(order)
    _list.add_card(name, description)


def _check_type_hook(response, expected_type):
    return response['action']['type'] == expected_type


def _get_order_id_from_card(response):
    card_name = response['action']['data']['card']['name']
    order_id = re.match(r'Заказ №(?P<id>\d+)', card_name, re.I)
    try:
        return int(order_id.groupdict()['id'])
    except (ValueError, AttributeError):
        return None


def _is_order_of_this_producer(producer_id, order_id):
    try:
        return producer_id == Order.query.get(order_id).producer_id
    except TypeError:
        return None


@celery.task
def change_order_status(response):
    if not _check_type_hook(response, 'updateCard'):
        return None
    try:
        new_status = response['action']['data']['listAfter']['name']
    except KeyError:
        return None
    board_id = response['action']['data']['board']['id']
    order_id = _get_order_id_from_card(response)
    if order_id is None:
        return
    producer = Producer.query.filter_by(trello_board_id=board_id).first()
    if producer is None:
        return None
    if not _is_order_of_this_producer(producer.id, order_id):
        return None
    Order.query.get(order_id).change_status(new_status)
    db.session.commit()

from trello import TrelloClient, ResourceUnavailable, Unauthorized
from contextlib import contextmanager
from flask import url_for
from marketplace.models import Producer, Product
from marketplace import app


@contextmanager
def authenticated(token):
    client = TrelloClient(api_key=app.config['TRELLO_API_KEY'], token=token)
    try:
        yield client
    except (ResourceUnavailable, Unauthorized):
        pass
    

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


def create_card_if_producer_linked_trello_account(producer_id, order, webhook=True):
    producer = Producer.query.get(producer_id)
    if producer is None or producer.trello_token is None:
        return
    with authenticated(producer.trello_token) as client:
        board = client.get_board(producer.trello_board_id)
        list_new = board.all_lists()[0]
        _add_card(order, list_new, client)
        if webhook:
            callback_url = url_for('.trellowebhook', _external=True)
            print('--------------------')
            print(callback_url)
            print('--------------------')
            print(client.create_hook(callback_url, board.id, client.resource_owner_key))
        
        

def _create_card_template(order):
    products = []
    print(order)
    
    for product_id, quantity in order.order_items_json.items():
        product = Product.query.get(product_id)
        products.append(f'> **Продукт**: {product.name}\n> **Артикул**: {product.id}\n> **Количество**: {quantity}\n')
    desc = f'\n```\nДоставка:  {order.delivery_method}\nПокупатель: {order.first_name} {order.last_name}\nАдрес: {order.delivery_address}\nТелефон: {order.consumer_phone}\nПочта: {order.consumer_email}\n```\n' 
    return '/n---/n'.join(products) + desc



def _add_card(order, _list, client):
    name = f'Заказ №{order.id}'
    description = _create_card_template(order)
    _list.add_card(name, description)

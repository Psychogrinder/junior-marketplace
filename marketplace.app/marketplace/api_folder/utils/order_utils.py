import json

from marketplace import db
from marketplace.api_folder.utils import product_utils
from marketplace.api_folder.utils.abortions import abort_if_producer_doesnt_exist_or_get, \
    abort_if_consumer_doesnt_exist_or_get, abort_if_order_doesnt_exist_or_get
from marketplace.models import Order


def get_orders_by_producer_id(producer_id):
    abort_if_producer_doesnt_exist_or_get(producer_id)
    return Order.query.filter_by(producer_id=producer_id).all()


def get_orders_by_consumer_id(consumer_id):
    abort_if_consumer_doesnt_exist_or_get(consumer_id)
    return Order.query.filter_by(consumer_id=consumer_id).all()


def get_order_by_id(order_id):
    return abort_if_order_doesnt_exist_or_get(order_id)


def get_all_products_from_order(order_id):
    order_items = Order.query.filter_by(id=order_id).first().order_items_json
    products = []
    for item in order_items:
        products.append(product_utils.get_product_by_id(product_id=int(item)))
    return products


def get_all_orders():
    return Order.query.all()


def post_orders(args):
    """
    Сначала обявляем переменные, которые содержат общую информацию. Затем работаем с каждым заказом отдельно.
    Для каждого заказа расчитываем итоговую стоимость, добавляем в заказ товары, у которых id производителя
    совпадает с id производителя заказа.
    :param args:
    :return:
    """
    abort_if_consumer_doesnt_exist_or_get(args['consumer_id'])
    # new_order = order_schema.load(args).data
    consumer_id = args['consumer_id']
    first_name = args['first_name']
    last_name = args['last_name']
    delivery_address = args['delivery_address']
    phone = args['phone']
    email = args['email']
    orders = args['orders']
    items = get_cart_by_consumer_id(consumer_id).items
    orders = json.loads(orders)
    for order in orders:
        total_cost = 0
        current_items = {}
        for product_id, quantity in items.items():
            product = get_product_by_id(int(product_id))
            if product.producer_id == int(order['producer_id']):
                current_items[product_id] = quantity
                total_cost += float(product.price.strip('₽').strip(' ')) * int(quantity)
        new_order = Order(total_cost, current_items, order['delivery_method'], delivery_address,
                          phone, email, consumer_id, order['producer_id'], first_name=first_name, last_name=last_name)
        db.session.add(new_order)
    clear_cart_by_consumer_id(consumer_id)
    db.session.commit()


def put_order(args, order_id):
    order = get_order_by_id(order_id)
    if args['status'] is not None:
        order.change_status(args['status'])
    db.session.commit()
    return order


def delete_order_by_id(order_id):
    order = get_order_by_id(int(order_id))
    db.session.delete(order)
    db.session.commit()
    return {"message": "Order with id {} has been deleted successfully".format(order_id)}


def get_number_of_unprocessed_orders_by_producer_id(producer_id):
    return len(Order.query.filter_by(producer_id=producer_id).filter_by(status='Необработан').all())

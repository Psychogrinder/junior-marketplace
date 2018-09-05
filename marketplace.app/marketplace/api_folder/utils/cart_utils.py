import json

from marketplace import db
from marketplace.api_folder.utils.abortions import abort_if_consumer_doesnt_exist_or_get, \
    abort_if_product_doesnt_exist_or_get
from marketplace.api_folder.utils.order_utils import get_order_by_id
from marketplace.api_folder.utils.product_utils import get_product_by_id
from marketplace.models import Cart, Order


def get_cart_by_consumer_id(consumer_id):
    abort_if_consumer_doesnt_exist_or_get(consumer_id)
    cart = Cart.query.filter_by(consumer_id=consumer_id).first()
    return cart if cart is not None else post_cart(consumer_id)


def get_number_of_products_in_cart(consumer_id):
    cart = Cart.query.filter_by(consumer_id=consumer_id).first()
    return sum(int(v) for k, v in cart.items.items()) if cart else 0


def get_products_from_cart(items):
    items = {int(k): int(v) for k, v in items.items()}
    products = [get_product_by_id(id) for id in items]
    return products


def post_cart(consumer_id):
    cart = Cart(consumer_id)
    db.session.add(cart)
    db.session.commit()
    return cart


def post_item_to_cart_by_consumer_id(args, consumer_id):
    abort_if_product_doesnt_exist_or_get(int(args['product_id']))
    cart = get_cart_by_consumer_id(consumer_id)
    if args['mode'] == 'inc':
        cart.increase_item_quantity(args['product_id'], args['quantity'])
    elif args['mode'] == 'dec':
        cart.decrease_item_quantity(args['product_id'], args['quantity'])
    elif args['mode'] == 'set':
        cart.set_item_quantity(args['product_id'], args['quantity'])
    db.session.commit()
    return cart


def remove_item_from_cart_by_consumer_id(args, consumer_id):
    abort_if_product_doesnt_exist_or_get(int(args['product_id']))
    cart = get_cart_by_consumer_id(consumer_id)
    cart.remove_item(args['product_id'])
    db.session.commit()
    return cart


def clear_cart_by_consumer_id(consumer_id):
    cart = get_cart_by_consumer_id(consumer_id)
    cart.clear_cart()
    db.session.commit()
    return {"message": "Cart has been cleared successfully".format(consumer_id)}


def decrease_products_quantity_and_increase_times_ordered(consumer_id):
    items = get_cart_by_consumer_id(consumer_id).items
    for item, quantity in items.items():
        get_product_by_id(int(item)).quantity -= int(quantity)
        get_product_by_id(int(item)).times_ordered += 1
        db.session.commit()


def increase_products_quantity_and_decrease_times_ordered(order_id):
    order = get_order_by_id(order_id)
    items = order.order_items_json
    for item, quantity in items.items():
        get_product_by_id(int(item)).quantity += int(quantity)
        get_product_by_id(int(item)).times_ordered -= 1
        db.session.commit()


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

from flask_restful import abort

from marketplace.models import Order, Consumer, Producer, Category, Product


def abort_if_order_doesnt_exist_or_get(order_id):
    order = Order.query.get(order_id)
    if order is None:
        abort(404, message='Order with id = {} doesn\'t exists'.format(order_id))
    return order


# def abort_if_consumer_doesnt_exist_or_get(consumer_id):
#     consumer = Consumer.query.filter_by(entity='consumer').filter_by(id=consumer_id).first()
#     if consumer is None:
#         abort(404, message='Consumer with id = {} doesn\'t exists'.format(consumer_id))
#     return consumer


# def abort_if_producer_doesnt_exist_or_get(producer_id):
#     producer = Producer.query.filter_by(entity='producer').filter_by(id=producer_id).first()
#     if producer is None:
#         abort(404, message='Producer with id = {} doesn\'t exists'.format(producer_id))
#     return producer


def abort_if_category_doesnt_exist_or_get(category_id):
    category = Category.query.get(category_id)
    if category is None:
        abort(404, message='Category with id = {} doesn\'t exists'.format(category_id))
    return category


def abort_if_category_doesnt_exist_slug_or_get(category_slug):
    category = Category.query.filter_by(slug=category_slug)
    if category is None:
        abort(404, message='Category with name = {} doesn\'t exists'.format(category_slug))
    return category


def abort_if_product_doesnt_exist_or_get(product):
    product = Product.query.get(product)
    if product is None:
        abort(404, message='Product with id = {} doesn\'t exists'.format(product))
    return product

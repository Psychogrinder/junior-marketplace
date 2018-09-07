from flask_restful import abort

from marketplace.models import Order, Consumer, Producer, Category, Product


def abort_if_order_doesnt_exist_or_get(order_id):
    order = Order.query.get(order_id)
    if order is None:
        abort(404, message='Order with id = {} doesn\'t exists'.format(order_id))
    return order


def abort_if_consumer_doesnt_exist_or_get(consumer_id):
    consumer = Consumer.query.filter_by(entity='consumer').filter_by(id=consumer_id).first()
    if consumer is None:
        abort(404, message='Consumer with id = {} doesn\'t exists'.format(consumer_id))
    return consumer


def abort_if_producer_doesnt_exist_or_get(producer_id):
    producer = Producer.query.filter_by(entity='producer').filter_by(id=producer_id).first()
    if producer is None:
        abort(404, message='Producer with id = {} doesn\'t exists'.format(producer_id))
    return producer


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


def failed_email_check(email):
    abort(406, message='Given email = \'{}\'  is invalid'.format(email))


def failed_password_len_check():
    abort(406, message='Given password is too short')


def failed_email_uniqueness_check(email):
    abort(406, message='User with given email = {} already exists'.format(email))


def failed_producer_name_uniqueness_check(name):
    abort(406, message='Producer with given name = {} already exists'.format(name))


def no_file_part_in_request():
    abort(406, message='No file part in request')


def no_image_presented():
    abort(406, message='No image presented')


def invalid_email_or_password():
    abort(406, message='Invalid email or password')


def admin_root_required():
    abort(403, message='Reject access')

from flask_restful import abort

from marketplace.models import Order, Consumer, Producer, Category, Product, Comment


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


def abort_if_product_doesnt_exist_or_get(product_id):
    product = Product.query.get(product_id)
    if product is None:
        abort(404, message='Product with id = {} doesn\'t exists'.format(product_id))
    return product


def abort_if_comment_doesnt_exist_or_get(comment_id):
    comment = Comment.query.get(comment_id)
    if comment is None:
        abort(404, message='Comment with id = {} doesn\'t exists'.format(comment_id))
    return comment


def abort_if_not_enough_products_or_get(product_id, quantity):
    product = abort_if_product_doesnt_exist_or_get(product_id)
    if product.quantity < quantity:
        abort(406, message='Товара {} в остатке меньше, чем вы заказали'.format(product.name))
    return product


def less_than_zero_items_in_carts():
    abort(406, message='Can\'t add negative number of elements to cart')


def failed_email_check(email):
    abort(406, message='Given email = \'{}\'  is invalid'.format(email))


def failed_password_len_check():
    abort(406, message='Given password is too short')


def failed_email_uniqueness_check():
    abort(406, message='Пользователь с таким email уже существует')


def failed_producer_name_uniqueness_check():
    abort(406, message='Магазин с таким названием уже существует')


def no_file_part_in_request():
    abort(406, message='No file part in request')


def no_image_presented():
    abort(406, message='No image presented')


def invalid_email_or_password():
    abort(406, message='Invalid email or password')


def admin_rights_required():
    abort(403, message='Reject access')


def account_access_denied():
    abort(403, message='Reject access to this page')

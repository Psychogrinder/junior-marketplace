from marketplace import email_tools, cache, REDIS_STORAGE_TIME
import os
import re
import json
import string
from flask_login import login_user, logout_user
from werkzeug.utils import secure_filename
from marketplace.api_folder.schemas import order_schema, consumer_sign_up_schema, producer_sign_up_schema, \
    product_schema, order_schema_list
from marketplace.models import Order, Consumer, Producer, Category, Product, Cart, User
from flask_restful import abort
from marketplace import db, app
from sqlalchemy import func, desc, exc
from sqlalchemy_searchable import inspect_search_vectors


# Abort methods

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


# Abort if methods


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


# Get by id methods

def get_orders_by_producer_id(producer_id):
    abort_if_producer_doesnt_exist_or_get(producer_id)
    return Order.query.filter_by(producer_id=producer_id).all()


def get_orders_by_consumer_id(consumer_id):
    abort_if_consumer_doesnt_exist_or_get(consumer_id)
    return Order.query.filter_by(consumer_id=consumer_id).all()


def get_order_by_id(order_id):
    return abort_if_order_doesnt_exist_or_get(order_id)


def get_consumer_by_id(consumer_id):
    return abort_if_consumer_doesnt_exist_or_get(consumer_id)


def get_producer_by_id(producer_id):
    return abort_if_producer_doesnt_exist_or_get(producer_id)


def get_category_by_id(category_id):
    return abort_if_category_doesnt_exist_or_get(category_id)


def get_subcategories_by_category_id(category_id):
    abort_if_category_doesnt_exist_or_get(category_id)
    return Category.query.filter_by(parent_id=category_id).all()


def get_subcategories_by_category_slug(category_slug):
    abort_if_category_doesnt_exist_slug_or_get(category_slug)
    category_id = Category.query.filter_by(slug=category_slug).first().id
    return Category.query.filter_by(parent_id=category_id).all()


def get_product_by_id(product_id):
    return abort_if_product_doesnt_exist_or_get(product_id)


def get_products_by_category_id(category_id):
    category = get_category_by_id(category_id)
    if category.parent_id != 0:
        return category.get_products()
    else:
        subcategories = get_subcategories_by_category_id(category_id)
        divided_products = [subcategory.get_products() for subcategory in subcategories]
        return [product for subcategory in divided_products for product in subcategory]


def get_products_by_producer_id(producer_id):
    abort_if_producer_doesnt_exist_or_get(producer_id)
    return Product.query.filter_by(producer_id=producer_id).all()


def get_cart_by_consumer_id(consumer_id):
    abort_if_consumer_doesnt_exist_or_get(consumer_id)
    cart = Cart.query.filter_by(consumer_id=consumer_id).first()
    return cart if cart is not None else post_cart(consumer_id)


def get_producer_name_by_id(producer_id):
    return db.session.query(Producer.name).filter(Producer.id == producer_id).first()


# Get by other params
def get_parent_category_by_category_id(category_id):
    parent_category_id = Category.query.filter_by(id=category_id).first().parent_id
    return get_category_by_id(parent_category_id)


def get_number_of_products_in_cart(consumer_id):
    items = Cart.query.filter_by(consumer_id=consumer_id).first().items
    return sum(int(v) for k, v in items.items())


def get_products_from_cart(items):
    items = {int(k): int(v) for k, v in items.items()}
    products = [get_product_by_id(id) for id in items]
    return products


def get_all_products_from_a_list_of_categories(categories):
    all_products = []
    for category in categories:
        all_products += category.get_products()
    return all_products


def get_products_from_a_parent_category(parent_category_id):
    subcategories = get_subcategories_by_category_id(parent_category_id)
    return get_all_products_from_a_list_of_categories(subcategories)


# Get by name

def get_category_by_name(slug):
    return Category.query.filter_by(slug=slug).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_producer_by_name(name):
    return Producer.query.filter_by(name=name).first()


def get_category_names_by_producer_name(producer_name):
    return [category.name for category in Producer.query.filter_by(name=producer_name).first().categories]


def get_subcategory_names_by_parent_category_slug_and_producer_name(parent_category_slug, producer_name):
    subcategories = get_subcategories_by_category_id(Category.query.filter_by(slug=parent_category_slug).first().id)
    all_producer_category_names = [category.name for category in
                                   Producer.query.filter_by(name=producer_name).first().categories]
    return [category.name for category in subcategories if category.name in all_producer_category_names]


def get_producer_names_by_category_name(category_name):
    category = Category.query.filter_by(name=category_name).first()
    producers = get_all_producers()
    return [producer.name for producer in producers if category in producer.categories]


def get_filtered_orders(args):
    order_status = args['order_status']
    if order_status == 'Все':
        orders = order_schema_list.dump(Order.query.filter_by(producer_id=int(args['producer_id'])).all()).data
    else:
        orders = order_schema_list.dump(
            Order.query.filter_by(producer_id=int(args['producer_id'])).filter_by(status=order_status).all()).data
    for order in orders:
        order['items'] = []
        order['order_timestamp'] = order['order_timestamp'].split('T')[0]
        for product_id, quantity in order['order_items_json'].items():
            product_data = db.session.query(Product.id, Product.name, Product.price, Product.weight,
                                            Product.photo_url, Product.measurement_unit).filter_by(id=int(product_id)).first()
            order_product_schema = ("id", "name", "price", "weight", "photo_url", "measurement_unit")
            product = dict(zip(order_product_schema, product_data))
            product['quantity'] = quantity
            if product['weight'].is_integer():
                product['weight'] = int(product['weight'])
            order['items'].append(product)
            del order['order_items_json']

    return orders


# Get sorted
def get_sorted_and_filtered_products(args):
    query = db.session.query(Product.id, Product.name, Product.price, Product.photo_url,
                             Producer.name.label('producer_name')).filter(
        Product.producer_id == Producer.id)

    if args['popularity']:
        if args['popularity'] == 'down':
            query = query.order_by(Product.times_ordered.desc())

    if args['producer_name']:
        query = query.filter(Producer.name == args['producer_name'])

    if args['in_stock'] == 1:
        query = query.filter(Product.quantity > 0)

    if args['category_name']:
        # check if the category_name is in English. Then it means it's a parent category
        if args['category_name'][0] in string.ascii_lowercase:
            parent_category_id = db.session.query(Category.id).filter(Category.slug == args['category_name']).first()
            subcategory_ids = [el[0] for el in
                               db.session.query(Category.id).filter(Category.parent_id == parent_category_id).all()]
            query = query.filter(Product.category_id.in_(subcategory_ids))
        # else it's a subcategory and the name is in Russian
        else:
            category_id = db.session.query(Category.id).filter(Category.name == args['category_name']).first()
            query = query.filter(Product.category_id == category_id)

    if args['price']:
        if args['price'] == 'down':
            query = query.order_by(Product.price.desc())
        elif args['price'] == 'up':
            query = query.order_by(Product.price.asc())

    product_schema = ("id", "name", "price", "photo_url", "producer_name")
    products_data = query.all()
    products = []
    for product_data in products_data:
        products.append(dict(zip(product_schema, product_data)))
    return products


def get_popular_products():
    return Product.query.order_by(Product.times_ordered.desc()).limit(12).all()


def get_popular_products_by_category_id(category_id, direction):
    """
    Если direction == up, то товары возврщаются от наименее популярных до самых популярных. Если down, то наоборот.
    """
    if direction == 'up':
        reverse = False
    elif direction == 'down':
        reverse = True

    if get_category_by_id(category_id).parent_id != 0:
        category = get_category_by_id(category_id)
        return sorted(category.get_products(), key=lambda product: int(product.times_ordered), reverse=reverse)
    else:
        all_products = get_products_from_a_parent_category(category_id)
        return sorted(all_products, key=lambda product: int(product.times_ordered), reverse=reverse)


def get_products_by_category_id_sorted_by_price(category_id, direction):
    """
    Если direction == up, то товары возврщаются от самых дешёвых до самых дорогих. Если down, то наоборот.
    """
    if direction == 'up':
        reverse = False
    elif direction == 'down':
        reverse = True

    if get_category_by_id(category_id).parent_id != 0:
        category = get_category_by_id(category_id)
        return sorted(category.get_products(), key=lambda product: float(product.price.strip('₽').strip(' ')),
                      reverse=reverse)
    else:
        all_products = get_products_from_a_parent_category(category_id)
        return sorted(all_products, key=lambda product: float(product.price.strip('₽').strip(' ')), reverse=reverse)


def get_all_products_from_order(order_id):
    order_items = Order.query.filter_by(id=order_id).first().order_items_json
    products = []
    for item in order_items:
        products.append(Product.query.filter_by(id=int(item)).first())
    return products


# Get all methods

def get_all_orders():
    return Order.query.all()


def get_all_consumers():
    return Consumer.query.filter_by(entity='consumer').all()


def get_all_producers():
    return Producer.query.filter_by(entity='producer').all()


def get_all_base_categories():
    return Category.query.filter_by(parent_id=0).all()


def get_all_products():
    return Product.query.all()


# Category methods
def delete_categories_if_it_was_the_last_product(product):
    quantity_of_products_with_this_category = len(Product.query.filter_by(producer_id=product.producer_id).filter_by(
        category_id=product.category_id).all())
    if quantity_of_products_with_this_category == 1:
        category = get_category_by_id(product.category_id)
        producer = get_producer_by_id(product.producer_id)
        producer.categories.remove(category)
        subcategories = get_subcategories_by_category_id(category.parent_id)
        has_such_categories = False
        for cat in subcategories:
            if cat in producer.categories:
                has_such_categories = True
                break
        if not has_such_categories:
            parent_category = get_category_by_id(category.parent_id)
            producer.categories.remove(parent_category)


def add_product_categories_if_producer_doesnt_have_them(product, new_category_id):
    producer = get_producer_by_id(product.producer_id)
    category = get_category_by_id(new_category_id)
    parent_category = get_category_by_id(category.parent_id)
    for category in (category, parent_category):
        if category not in producer.categories:
            producer.categories.append(category)


def check_producer_categories(new_category_id, product):
    if product.category_id != int(new_category_id):
        delete_categories_if_it_was_the_last_product(product)
        add_product_categories_if_producer_doesnt_have_them(product, new_category_id)


# Product methods

def producer_has_product_with_such_name(args):
    if Product.query.filter_by(producer_id=args['producer_id']).filter_by(name=args['name']).first():
        return True


def search_products_by_param(search_query):
    vector = inspect_search_vectors(Product)[0]
    try:
        result = db.session.query(Product).filter(
            Product.search_vector.match(search_query)
        ).order_by(desc(func.ts_rank_cd(vector, func.tsq_parse(search_query)))).all()
    except exc.ProgrammingError:
        return None
    return result


# Post methods

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
            if Product.query.get(int(product_id)).producer_id == int(order['producer_id']):
                current_items[product_id] = quantity
                total_cost += float(Product.query.get(int(product_id)).price.strip('₽').strip(' ')) * int(quantity)
        new_order = Order(total_cost, current_items, order['delivery_method'], delivery_address,
                          phone, email, consumer_id, order['producer_id'], first_name=first_name, last_name=last_name)
        db.session.add(new_order)
    clear_cart_by_consumer_id(consumer_id)
    db.session.commit()


def post_consumer(args):
    validate_registration_data(args['email'], args['password'])
    check_email_uniqueness(args['email'])
    new_consumer = consumer_sign_up_schema.load(args).data
    db.session.add(new_consumer)
    db.session.commit()
    email_tools.send_confirmation_email(new_consumer.email)
    return new_consumer


def post_producer(args):
    validate_registration_data(args['email'], args['password'])
    check_email_uniqueness(args['email'])
    check_producer_name_uniqueness(args['name'])
    new_producer = producer_sign_up_schema.load(args).data
    db.session.add(new_producer)
    db.session.commit()
    email_tools.send_confirmation_email(new_producer.email)
    return new_producer


def post_product(args):
    abort_if_producer_doesnt_exist_or_get(args['producer_id'])
    abort_if_category_doesnt_exist_or_get(args['category_id'])
    new_product = product_schema.load(args).data
    db.session.add(new_product)
    producer = get_producer_by_id(args['producer_id'])
    category = get_category_by_id(args['category_id'])
    parent_category = get_category_by_id(category.parent_id)
    for category in (category, parent_category):
        if category not in producer.categories:
            producer.categories.append(category)
    db.session.commit()
    return new_product


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


# Put methods

def put_order(args, order_id):
    order = get_order_by_id(order_id)
    if args['status'] is not None:
        order.change_status(args['status'])
    db.session.commit()
    return order


def put_producer(args, producer_id):
    producer = get_producer_by_id(producer_id)
    args['id'] = None
    for k, v in args.items():
        if v:
            setattr(producer, k, v)
    db.session.commit()
    return producer


def put_consumer(args, consumer_id):
    consumer = get_consumer_by_id(consumer_id)
    args['id'] = None
    for k, v in args.items():
        if v:
            setattr(consumer, k, v)
    db.session.commit()
    return consumer


def put_product(args, product_id):
    product = get_product_by_id(product_id)

    if args['category_id']:
        check_producer_categories(args['category_id'], product)

    args['id'] = None
    args['producer_id'] = None
    for k, v in args.items():
        if v:
            setattr(product, k, v)
    db.session.commit()
    return product


# Delete methods

def delete_consumer_by_id(consumer_id):
    consumer = get_consumer_by_id(consumer_id)
    db.session.delete(consumer)
    db.session.commit()
    return {"message": "Consumer with id {} has been deleted".format(consumer_id)}


def delete_producer_by_id(producer_id):
    producer = get_producer_by_id(producer_id)
    db.session.delete(producer)
    db.session.commit()
    return {"message": "Producer with id {} has been deleted successfully".format(producer_id)}


def delete_product_by_id(product_id):
    product = get_product_by_id(product_id)
    delete_categories_if_it_was_the_last_product(product)
    db.session.delete(product)
    db.session.commit()
    return {"message": "Product with id {} has been deleted successfully".format(product_id)}


def delete_order_by_id(order_id):
    order = get_order_by_id(int(order_id))
    db.session.delete(order)
    db.session.commit()
    return {"message": "Order with id {} has been deleted successfully".format(order_id)}


def clear_cart_by_consumer_id(consumer_id):
    cart = get_cart_by_consumer_id(consumer_id)
    cart.clear_cart()
    db.session.commit()
    return {"message": "Cart has been cleared successfully".format(consumer_id)}


# Login/Logout

def login(args):
    user = User.query.filter_by(email=args['email']).first()
    if user is None or not user.check_password(args['password']):
        return False
    # Вместо True потом добавить возможность пользователю выбирать запоминать его или нет
    login_user(user, True)
    return {"id": user.id, "entity": user.entity}


def logout():
    logout_user()
    return 'Logout'


# Validation

def validate_registration_data(email, password):
    email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_pattern, email):
        failed_email_check(email)
    if len(password) < 6:
        failed_password_len_check()
    return True


# Checkers

def check_email_uniqueness(email):
    if get_user_by_email(email) is not None:
        failed_email_uniqueness_check(email)


def check_producer_name_uniqueness(name):
    if get_producer_by_name(name) is not None:
        failed_producer_name_uniqueness_check(name)


# Orders

def get_number_of_unprocessed_orders_by_producer_id(producer_id):
    return len(Order.query.filter_by(producer_id=producer_id).filter_by(status='Необработан').all())


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


# Uploaders

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image(uploader, files):
    if 'image' not in files:
        no_file_part_in_request()
    image = files['image']
    if image.filename == '':
        no_image_presented()
    if image and allowed_extension(image.filename):
        image_url = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
        image.save(image_url)
        uploader.set_photo_url(image_url)
        db.session.commit()
    return True


def upload_consumer_image(consumer_id, files):
    consumer = get_consumer_by_id(consumer_id)
    return upload_image(consumer, files)


def upload_producer_image(producer_id, files):
    producer = get_producer_by_id(producer_id)
    return upload_image(producer, files)


def upload_product_image(product_id, files):
    product = get_product_by_id(product_id)
    return upload_image(product, files)


# Caching

def cache_json_and_get(path, response):
    cache.execute_command('JSON.SET', path, '.', json.dumps(response))
    cache.expire(path, REDIS_STORAGE_TIME)
    return response

def get_cached_json(path):
    res = cache.execute_command('JSON.GET', path, 'NOESCAPE')
    return json.loads(res) if res is not None else None



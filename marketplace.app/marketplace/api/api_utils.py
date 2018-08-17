from operator import itemgetter
from marketplace.models import Order, Consumer, Producer, Category, Product
from flask_restful import abort
from marketplace.marshmallow_schemas import OrderSchema, ConsumerSchema, ProducerSchema, CategorySchema, ProductSchema
from marketplace import db

# Marshmallow schemas

order_schema = OrderSchema()
consumer_schema = ConsumerSchema()
producer_schema = ProducerSchema()
category_schema = CategorySchema()
product_schema = ProductSchema()
order_schema_list = OrderSchema(many=True)
consumer_schema_list = ConsumerSchema(many=True)
producer_schema_list = ProducerSchema(many=True)
category_schema_list = CategorySchema(many=True)
product_schema_list = ProductSchema(many=True)


# Abort methods


def abort_if_order_doesnt_exist(order_id):
    if Order.query.get(order_id) is None:
        abort(404, message='Order with id = {} doesn\'t exists'.format(order_id))


def abort_if_consumer_doesnt_exist(consumer_id):
    if Consumer.query.get(consumer_id) is None:
        abort(404, message='Consumer with id = {} doesn\'t exists'.format(consumer_id))


def abort_if_producer_doesnt_exist(producer_id):
    if Producer.query.get(producer_id) is None:
        abort(404, message='Producer with id = {} doesn\'t exists'.format(producer_id))


def abort_if_category_doesnt_exist(category_id):
    if Category.query.get(category_id) is None:
        abort(404, message='Category with id = {} doesn\'t exists'.format(category_id))


def abort_if_product_doesnt_exist(product):
    if Product.query.get(product) is None:
        abort(404, message='Product with id = {} doesn\'t exists'.format(product))


# Get by id methods

def get_orders_by_producer_id(producer_id):
    abort_if_producer_doesnt_exist(producer_id)
    return order_schema_list.dump(Order.query.filter_by(producer_id=producer_id).all()).data


def get_orders_by_consumer_id(consumer_id):
    abort_if_consumer_doesnt_exist(consumer_id)
    return order_schema_list.dump(Order.query.filter_by(consumer_id=consumer_id).all()).data


def get_order_by_id(order_id):
    abort_if_order_doesnt_exist(order_id)
    return order_schema.dump(Order.query.get(order_id)).data


def get_consumer_by_id(consumer_id):
    abort_if_consumer_doesnt_exist(consumer_id)
    return Consumer.query.get(consumer_id)


def get_producer_by_id(producer_id):
    abort_if_producer_doesnt_exist(producer_id)
    return Producer.query.get(producer_id)


def get_category_by_id(category_id):
    abort_if_category_doesnt_exist(category_id)
    return Category.query.get(category_id)


def get_subcategories_by_category_id(category_id):
    abort_if_category_doesnt_exist(category_id)
    return Category.query.fileter_by(parent_id=category_id).all()


def get_product_by_id(product_id):
    abort_if_product_doesnt_exist(product_id)
    return Product.query.get(product_id)


def get_products_by_category_id(category_id):
    category = get_category_by_id(category_id)
    if category.parent_id != 0:
        return producer_schema_list.dump(category.get_products()).data
    else:
        subcategories = get_subcategories_by_category_id(category_id)
        divided_products = [product_schema_list.dump(subcategory.get_products()).data for subcategory in subcategories]
        return [product for subcategory in divided_products for product in subcategory]


def get_products_by_producer_id(producer_id):
    producer = get_producer_by_id(producer_id)
    return product_schema_list.dumo(producer.get_products())


# Get sorted


def get_popular_products_by_category_id(category_id):
    category = get_category_by_id(category_id)
    return sorted(product_schema_list.dump(category.get_products()).data,
                  key=itemgetter('times_ordered'), reverse=True)


def get_popular_products():
    return sorted(get_all_products(), key=itemgetter('times_ordered'), reverse=True)


# Get all methods

def get_all_orders():
    return order_schema_list.dump(Order.query.all()).data


def get_all_consumers():
    return consumer_schema_list.dump(Consumer.query.filter_by(entity='consumer').all()).data


def get_all_producers():
    return producer_schema_list.dump(Producer.query.filter_by(entity='producer').all()).data


def get_all_default_categories():
    return category_schema_list.dump(Category.query.fileter_by(parent_id=0).all()).data


def get_all_products():
    return product_schema_list.dump(Product.query.all()).data


# Post methods

def post_order(args):
    abort_if_producer_doesnt_exist(args['producer_id'])
    abort_if_consumer_doesnt_exist(args['consumer_id'])
    new_order = order_schema.load(args).data
    db.session.add(new_order)
    db.session.commit()
    return order_schema.dump(new_order).data


def post_consumer(args):
    new_consumer = consumer_schema.load(args).data
    new_consumer.set_password(args['password'])
    db.session.add(new_consumer)
    db.session.commit()
    return consumer_schema.dump(new_consumer).data


def post_producer(args):
    new_producer = producer_schema.load(args).data
    new_producer.set_password(args['password'])
    db.session.add(new_producer)
    db.session.commit()
    return producer_schema.dump(new_producer).data


def post_product(args):
    abort_if_producer_doesnt_exist(['producer_id'])
    abort_if_category_doesnt_exist(['category_id'])
    new_product = product_schema.load(args).data
    db.session.add(new_product)
    db.session.commit()
    return order_schema.dump(new_product).data


# Put methods

def put_order(args, order_id):
    order = get_order_by_id(order_id)
    if args['status'] is not None:
        order.change_status(args['status'])
    db.session.commit()
    return order_schema.dump(order).data


def put_producer(args, producer_id):
    producer = get_producer_by_id(producer_id)
    # Изменяет producer, но мы пока не придумали как именно
    db.session.commit()
    return producer_schema.dump(producer).data


def put_consumer(args, consumer_id):
    consumer = get_consumer_by_id(consumer_id)
    # Изменяет consumer, но мы пока не придумали как именно
    db.session.commit()
    return consumer_schema.dump(consumer).data


def put_product(args, product_id):
    product = get_product_by_id(product_id)
    # Изменяет product, но мы пока не придумали как именно
    db.session.commit()
    return product_schema.dump(product).data


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
    return {"message": "Producer with id {} has been deleted succesfully".format(producer_id)}


def delete_product_by_id(product_id):
    product = get_product_by_id(product_id)
    db.session.delete(product)
    db.session.commit()
    return {"message": "Product with id {} has been deleted succesfully".format(product_id)}


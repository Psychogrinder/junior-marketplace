import os

from sqlalchemy import JSON
from sqlalchemy.ext.mutable import MutableDict

try:
    from marketplace import db, login
except:
    from content.data_app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.dialects.postgresql import MONEY
from flask_login import UserMixin

producer_category_association_table = db.Table('producers_categories',
                                               db.Column('producer_id', db.Integer, db.ForeignKey('user.id'),
                                                         primary_key=True),
                                               db.Column('category_id', db.Integer, db.ForeignKey('category.id'),
                                                         primary_key=True)
                                               )


class SetPhotoUrlMixin():
    def set_photo_url(self, photo_url):
        if self.photo_url is None:
            self.photo_url = photo_url
        elif self.photo_url is not None and self.photo_url != photo_url:
            os.remove(self.photo_url)
            self.photo_url = photo_url


class User(SetPhotoUrlMixin, UserMixin, db.Model):
    __tablename__ = 'user'
    __mapper_args = {'polymorphic_on': 'discriminator'}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    email_auth_status = db.Column(db.Boolean)
    password_hash = db.Column(db.String(1024))
    phone_number = db.Column(db.String(16))
    address = db.Column(db.String(128))
    photo_url = db.Column(db.String(256))
    entity = db.Column(db.String(16))

    def __init__(self, email, password, entity, phone_number='', address=''):
        self.email = email
        self.email_auth_status = False
        self.phone_number = get_string_or_default(phone_number)
        self.password_hash = generate_password_hash(password)
        self.address = get_string_or_default(address)
        self.entity = entity

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def change_password(self, old_password, new_password):
        if check_password_hash(self.password_hash, old_password):
            self.password_hash = generate_password_hash(new_password)
            return True
        else:
            return False

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_email(self):
        self.email_auth_status = True

    def set_address(self, address):
        self.address = address

    def set_phone(self, phone_number):
        self.phone_number = phone_number


class Consumer(User):
    __mapper_args__ = {'polymorphic_identity': 'consumer'}
    last_name = db.Column(db.String(128))
    patronymic = db.Column(db.String(128))
    first_name = db.Column(db.String(128))

    def __init__(self, email, password, first_name, last_name, phone_number, address, patronymic=''):
        super().__init__(email, password, 'consumer', phone_number, address)
        self.first_name = get_string_or_default(first_name)
        self.last_name = get_string_or_default(last_name)
        self.patronymic = get_string_or_default(patronymic)

    def get_orders(self):
        return Order.query.filter_by(consumer_id=self.id).all()

    def get_full_name(self):
        return "{first_name} {patronymic} {last_name}".format(first_name=self.first_name, patronymic=self.patronymic,
                                                              last_name=self.last_name).strip()


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consumer_id = db.Column(db.Integer)
    items = db.Column(MutableDict.as_mutable(JSON), server_default='{}', nullable=False, default={})

    def __init__(self, consumer_id):
        self.consumer_id = consumer_id

    def put_item(self, product_id, quantity):
        if product_id not in self.items.keys():
            self.items[product_id] = int(quantity)
        else:
            self.items[product_id] += int(quantity)

    def remove_item(self, product_id):
        self.items.pop(product_id, None)

    def clear_cart(self):
        self.items.clear()


class Producer(User):
    __mapper_args__ = {'polymorphic_identity': 'producer'}
    name = db.Column(db.String(128), unique=True)
    person_to_contact = db.Column(db.String(128))
    description = db.Column(db.String(256))
    categories = db.relationship(
        "Category",
        secondary=producer_category_association_table,
        lazy='subquery',
        backref=db.backref('producers', lazy=True))

    def __init__(self, password, email, name, phone_number, address, person_to_contact, description=''):
        super().__init__(email, password, 'producer', phone_number, address)
        self.name = name
        self.person_to_contact = person_to_contact
        self.description = get_string_or_default(description)

    def get_products(self):
        return Product.query.filter_by(producer_id=self.id).all()

    def get_orders(self):
        return Product.query.filter_by(producer_id=self.id).all()

    def set_description(self, description):
        self.description = description


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_cost = db.Column(MONEY)
    order_items_json = db.Column(db.JSON)
    status = db.Column(db.String(128))
    delivery_method = db.Column(db.String(128))
    delivery_address = db.Column(db.String(128))
    order_timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    shipping_timestamp = db.Column(db.DateTime)
    consumer_phone = db.Column(db.String(128))
    consumer_email = db.Column(db.String(128))
    consumer_id = db.Column(db.Integer)
    producer_id = db.Column(db.Integer)

    def __init__(self, total_cost, order_items_json, delivery_method, delivery_address, consumer_phone, consumer_email,
                 consumer_id, producer_id, status='not processed'):
        self.total_cost = int(total_cost)
        self.order_items_json = order_items_json
        self.status = status
        self.delivery_method = delivery_method
        self.delivery_address = delivery_address
        self.consumer_id = consumer_id
        self.producer_id = producer_id
        self.consumer_phone = consumer_phone
        self.consumer_email = consumer_email

    def get_consumer(self):
        return Consumer.query.filter_by(id=self.consumer_id).first()

    def get_producer(self):
        return Producer.query.filter_by(id=self.producer_id).first()

    def change_status(self, status):
        if status == 'shipped':
            self.shipping_timestamp = datetime.utcnow()
        self.status = status


class Product(SetPhotoUrlMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(256))
    photo_url = db.Column(db.String(256))
    price = db.Column(MONEY)
    quantity = db.Column(db.Integer)
    times_ordered = db.Column(db.Integer)
    producer_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    measurement_unit = db.Column(db.String(16))
    weight = db.Column(db.Float)

    def __init__(self, price, name, quantity, producer_id, category_id, measurement_unit, weight, description=''):
        self.price = float(price)
        self.name = name
        self.quantity = quantity
        self.producer_id = producer_id
        self.category_id = category_id
        self.measurement_unit = measurement_unit
        self.times_ordered = 0
        self.weight = weight
        self.description = get_string_or_default(description)

    def set_description(self, description):
        self.description = description

    def get_producer(self):
        return Producer.query.filter_by(id=self.producer_id).all()

    def get_category(self):
        return Category.query.filter_by(id=self.category_id).all()


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    slug = db.Column(db.String(128))
    parent_id = db.Column(db.Integer)

    def __init__(self, name, slug=None, parent_id=0):
        self.name = name
        self.slug = slug
        self.parent_id = parent_id

    def get_products(self):
        return Product.query.filter_by(category_id=self.id).all()

    def get_subcategories(self):
        return Category.query.filter_by(parent_id=self.id).all()


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def get_string_or_default(item):
    return item if item is not None else ''

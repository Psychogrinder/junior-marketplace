from app.models import Order, Product, Consumer, Producer, Category
from app import ma
from marshmallow import fields, post_load
from marshmallow_sqlalchemy import ModelConverter
from sqlalchemy.dialects.postgresql import MONEY


class PostgresMoneyConverter(ModelConverter):
    SQLA_TYPE_MAPPING = dict(
        list(ModelConverter.SQLA_TYPE_MAPPING.items()) +
        [(MONEY, fields.Str)]
    )


class OrderSchema(ma.ModelSchema):
    class Meta:
        model = Order
        model_converter = PostgresMoneyConverter

        @post_load
        def create_order(self, data):
            return Order(**data)


class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product
        model_converter = PostgresMoneyConverter

        @post_load
        def create_product(self, data):
            return Product(**data)


class ConsumerSchema(ma.ModelSchema):
    class Meta:
        model = Consumer
        fields = ('id', 'email', 'name', 'person_to_contact', 'description', 'phone_number', 'address')

        @post_load
        def create_consumer(self, data):
            return Order(**data)


class ProducerSchema(ma.ModelSchema):
    class Meta:
        model = Producer
        fields = ('id', 'email', 'first_name', 'patronymic', 'last_name', 'phone_number', 'address')

        @post_load
        def create_producer(self, data):
            return Producer(**data)


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category
        
        @post_load
        def create_category(self, data):
            return Category(**data)


from marketplace.models import Order, Product, Consumer, Producer, Category
from marketplace import ma
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


class ConsumerSignUpSchema(ma.ModelSchema):
    class Meta:
        model = Consumer
        fields = ('id', 'email', 'password', 'first_name', 'patronymic', 'last_name', 'phone_number', 'address')


class ProducerSignUpSchema(ma.ModelSchema):
    class Meta:
        model = Producer
        fields = ('id', 'email', 'password', 'name', 'person_to_contact', 'description', 'phone_number', 'address')


class ConsumerSchema(ma.ModelSchema):
    class Meta:
        model = Consumer
        fields = ('id', 'email', 'first_name', 'patronymic', 'last_name', 'phone_number', 'address')


class ProducerSchema(ma.ModelSchema):
    class Meta:
        model = Producer
        fields = ('id', 'email', 'name', 'person_to_contact', 'description', 'phone_number', 'address')


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category

        @post_load
        def create_category(self, data):
            return Category(**data)

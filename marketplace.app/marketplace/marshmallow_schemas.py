from marketplace.models import Order, Product, Consumer, Producer, Category
from marketplace import ma
from marshmallow import fields
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


class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product
        model_converter = PostgresMoneyConverter


class ConsumerSchema(ma.ModelSchema):
    class Meta:
        model = Consumer
        fields = ('id', 'email', 'name', 'person_to_contact', 'description', 'phone_number', 'address')


class ProducerSchema(ma.ModelSchema):
    class Meta:
        model = Producer
        fields = ('id', 'email', 'first_name', 'patronymic', 'last_name', 'phone_number', 'address')


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category


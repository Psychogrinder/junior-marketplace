from app.models import Order, Product, Consumer, Producer, Category
from app import ma
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


class ProducerSchema(ma.ModelSchema):
    class Meta:
        model = Producer


class CategorySchema(ma.ModelSchema):
    class Meta:
        model = Category


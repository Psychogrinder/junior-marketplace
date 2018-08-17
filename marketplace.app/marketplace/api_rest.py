from marketplace.models import Product, Category, db
from marketplace.marshmallow_schemas import CategorySchema, ProductSchema
from marketplace import api
from flask_restful import Resource, reqparse
from operator import itemgetter
parser = reqparse.RequestParser()
for arg in ['price', 'name', 'quantity', 'producer_id', 'category_id', 'measurement_unit', 'weight', 'description']:
    parser.add_argument(arg)

def get_category_by_name(category_name):
    return Category.query.filter_by(name=category_name).first()


def get_category_by_id(category_id):
    return Category.query.filter_by(id=category_id).first()


def get_subcategory_names(category_id):
    category = get_category_by_id(category_id)
    subcategories = category.get_subcategories()
    return [obj.name for obj in subcategories]


def abort_if_category_doesnt_exist(id):
    if not Category.query.filter_by(id=id).first():
        abort(404, message="Category with id {} doesn't exists".format(id))


def abort_if_producer_doesnt_exist(id):
    if not Producer.query.filter_by(id=id).first():
        abort(404, message="No producer with id {}".format(id))


def abort_if_product_doesnt_exist(id):
    if not Product.query.filter_by(id=id).first():
        abort(404, message="No product with id {}".format(id))

class BaseCategories(Resource):
    """
    Возвращает список имён базовых категорий.
    """
    def get(self):
        base_categories = Category.query.filter_by(parent_id=0).all()
        return {
            'base_categories': [category.name for category in base_categories]
        }

class Subcategories(Resource):
    def get(self, id):
        abort_if_category_doesnt_exist(id)
        category = get_category_by_id(id)
        return {
            'category_id': category.id,
            'subcategories': get_subcategory_names(category.id)
        }


class ProductsByCategory(Resource):
    def get(self, id):
        abort_if_category_doesnt_exist(id)
        category = get_category_by_id(id)
        product_schema = ProductSchema(many=True)
        if category.parent_id != 0:
            products = product_schema.dump(category.get_products())
        else:
            subcategories = Category.query.filter_by(parent_id=category.id).all()
            divided_products = [product_schema.dump(subcategory.get_products()).data for subcategory in subcategories]
            products = [product for subcategory in divided_products for product in subcategory]
        return {
            'category_id': category.id,
            'products': products
        }


class ProductsByProducer(Resource):
    def get(self, id):
        abort_if_producer_doesnt_exist(id)
        producer = Producer.query.filter_by(id=id).first()
        product_schema = ProductSchema(many=True)
        return {
            'producer': producer.name,
            'products': product_schema.dump(producer.get_products())
        }


class ProductsByPopularity(Resource):
    """
    Первыми идут самые популярные.
    """
    def get(self, id):
        abort_if_category_doesnt_exist(id)
        category = get_category_by_id(id)
        products = category.get_products()

        product_schema = ProductSchema(many=True)
        products = product_schema.dump(products).data
        products = sorted(products, key=itemgetter('times_ordered'), reverse=True)
        return {
            'producer': category.id,
            'products': products
        }


class ProductRest(Resource):
    def get(self, id):
        """
        :param id:
        :return: карточка продукта по id
        """
        abort_if_product_doesnt_exist(id)
        product = Product.query.filter_by(id=id).first()
        product_schema = ProductSchema(many=True)
        return product_schema.dump(product)

    def delete(self, id):
        """
        Удаляет товар по id
        """
        abort_if_product_doesnt_exist(id)
        Product.query.filter_by(id=id).delete()
        db.session.commit()
        return {"message": "Продукт с id {} был успешно удалён.".format(id)}

    def put(self, id):
        """
        Обновить информацию о продукте
        """
        abort_if_product_doesnt_exist(id)
        product = Product.query.filter_by(id=id).first()
        args = parser.parse_args()
        for key, value in args.items():
            print(key, value)
            if value is not None:
                setattr(product, key, value)
        db.session.commit()

        return {"message": "Продукт был успешно отредактирован."}

    def post(self):
        """
        Добавить продукт
        """
        args = parser.parse_args()
        schema = ProductSchema()
        product = schema.load(args).data
        db.session.add(product)
        db.session.commit()

        return {"message": "Продукт был успешно добавлен."}

api.add_resource(BaseCategories, '/category/base')
api.add_resource(Subcategories, '/category/subcategories/<int:id>')
api.add_resource(ProductsByCategory, '/category/<int:id>')
api.add_resource(ProductsByPopularity, '/category/popularity/<int:id>')
api.add_resource(ProductsByProducer, '/producer/<int:id>')
api.add_resource(ProductRest, '/product/<int:id>', "/product")
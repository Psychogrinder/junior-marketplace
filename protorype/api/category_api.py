from flask_restful import Resource, Api
from app.models import Category
from app.models import Product
from flask import jsonify

api = Api(app)


# но зачем?
class CategoryNameById(Resource):
    def get(self, num):
        # вернуть название категории по id
        category = Category.query.filter_by(id=id).first()
        if category:
            return {'description': 'category data', 'data': {'id': num, 'name': category.name}}
        else:
            return {'error': 'No category with such id'}, 404


class CategoryProducts(Resource):
    def get(self, category_name):
        """
        :return: JSON с товарами из данной подкатегории
        """
        category = Category.query.filter_by(name=category_name).first()
        if category:
            # products: список с id продуктов
            products = jsonify([item.to_json() for item in Product.query.filter(producer_id=category.id).all()])
            return {'category_name': category_name, 'products': products}
        else:
            return {'error': 'No category with such name'}, 404


class SubcategoryProducts(Resource):
    def get(self, category_name, subcategory_name):
        """
        :return: JSON с товарами из данной подкатегории
        """
        category = Category.query.filter_by(name=category_name).first()
        if category:
            subcategory = Category.query.filter_by(name=subcategory_name).first()
            if subcategory:
                if subcategory.parent == category.id:
                    products = jsonify([item.to_json() for item in Product.query.filter(producer_id=subcategory.id).all()])
                    return {'subcategory_name': subcategory_name, 'products': products}
                else:
                    return {'error': f'Category {category_name} does not have a subcategory {subcategory_name}'}, 404
            else:
                return {'error': 'No category with such name'}, 404
        else:
            return {'error': 'No category with such name'}, 404


api.add_resource(CategoryNameById, '/category/<int:num>')
api.add_resource(CategoryProducts, '/category/<string:category_name>/')
api.add_resource(SubcategoryProducts, '/category/<string:category_name>/<string:subcategory_name>/')

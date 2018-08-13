from flask_restful import Resource, Api
from marketplace.app.marketplace import Category as dbCategory

api = Api(app)

# но зачем?
class CategoryNameById(Resource):
    def get(self, num):
        # вернуть название категории по id
        name = dbCategory.query.filter_by(dbCategory.id == id).first()
        if name:
            return {'description':'category data', 'data': {'id': num, 'name': name}}
        else:
            return {'error': 'No category with such id'}, 404

class CategoryProducts(Resource):
    def get(self, category_name):
        """
        :return: JSON с товарами из данной подкатегории
        """
        category = dbCategory.query.filter_by(name=category_name).first()
        if category:
            # products: список с id продуктов
            products = category.products
            # TODO products: словарь с продуктами
            products = None
            return {'category_name': name, 'products': products}
        else:
            return {'error': 'No category with such name'}, 404

class SubcategoryProducts(Resource):
    def get(self, category_name, subcategory_name):
        """
        :return: JSON с товарами из данной подкатегории
        """
        category = dbCategory.query.filter_by(name=category_name).first()
        if category:
            subcategory = dbCategory.query.filter_by(name=subcategory_name).first()
            if subcategory:
                # Если родительская категория подкатегории = имя категории
                if subcategory.parent_category == category.name:
                    # products: список с id продуктов
                    products = subcategory.products
                    # TODO products: словарь с продуктами
                    products = None
                    return {'category_name': name, 'products': products}
                else:
                    return {'error': f'Category {category_name} does not have a subcategory {subcategory_name}'}, 404
            else:
                return {'error': 'No category with such name'}, 404
        else:
            return {'error': 'No category with such name'}, 404

api.add_resource(CategoryNameById, '/category/<int:num>')
api.add_resource(CategoryProducts, '/category/<string:category_name>/')
api.add_resource(SubcategoryProducts, '/category/<string:category_name>/<string:subcategory_name>/')

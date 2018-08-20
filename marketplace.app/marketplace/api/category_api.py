import marketplace.api.api_utils as utils
from flask_restful import Resource


class BaseCategories(Resource):
    def get(self):
        return utils.get_all_default_categories()


class Subcategories(Resource):
    def get(self, category_id):
        return utils.get_subcategories_by_category_id(category_id)


class ProductsByCategory(Resource):
    def get(self, category_id):
        return utils.get_products_by_category_id(category_id)


class PopularProductsByCategory(Resource):
    def get(self, category_id):
        return utils.get_popular_products_by_category_id(category_id)

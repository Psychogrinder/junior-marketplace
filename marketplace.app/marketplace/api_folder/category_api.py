import marketplace.api_folder.api_utils as utils
from flask_restful import Resource

from marketplace.api_folder.schemas import category_schema_list, product_schema_list, category_schema


class CategoryRest(Resource):
    def get(self, slug):
        return category_schema.dump(utils.get_category_by_name(slug)).data

class BaseCategories(Resource):
    def get(self):
        return category_schema_list.dump(utils.get_all_base_categories()).data


class Subcategories(Resource):
    def get(self, category_id):
        return category_schema_list.dump(utils.get_subcategories_by_category_id(category_id)).data

class SubcategoriesBySlug(Resource):
    def get(self, category_slug):
        return category_schema_list.dump(utils.get_subcategories_by_category_slug(category_slug)).data

class ProductsByCategory(Resource):
    def get(self, category_id):
        return product_schema_list.dump(utils.get_products_by_category_id(category_id)).data


class PopularProductsByCategory(Resource):
    def get(self, category_id, direction):
        return product_schema_list.dump(utils.get_popular_products_by_category_id(category_id, direction)).data

class ParentCategoryBySubcategoryId(Resource):
    def get(self, category_id):
        return category_schema.dump(utils.get_parent_category_by_category_id(category_id)).data
from flask import request

import marketplace.api_folder.api_utils as utils
from flask_restful import Resource

from marketplace.api_folder.schemas import category_schema_list, product_schema_list, category_schema


class CategoryRest(Resource):
    def get(self, slug):
        return category_schema.dump(utils.get_category_by_name(slug)).data


class BaseCategories(Resource):
    def get(self):
        response = dict()
        page_number = request.args.get('page', type=int, default=1)
        page = utils.get_all_base_categories(page_number)
        response['meta'] = utils.get_meta_from_page(page_number, page)
        response['body'] = category_schema_list.dump(page.items).data
        return response, 200


class Subcategories(Resource):
    def get(self, category_id):
        response = dict()
        page_number = request.args.get('page', type=int, default=1)
        page = utils.get_subcategories_by_category_id(category_id, page_number)
        response['meta'] = utils.get_meta_from_page(page_number, page)
        response['body'] = category_schema_list.dump(page.items).data
        return response, 200


class SubcategoriesBySlug(Resource):
    def get(self, category_slug):
        response = dict()
        page_number = request.args.get('page', type=int, default=1)
        page = utils.get_subcategories_by_category_slug(category_slug, page_number)
        response['meta'] = utils.get_meta_from_page(page_number, page)
        response['body'] = category_schema_list.dump(page.items).data
        return response, 200


class ProductsByCategory(Resource):
    def get(self, category_id):
        return product_schema_list.dump(utils.get_products_by_category_id(category_id)).data


class PopularProductsByCategory(Resource):
    def get(self, category_id, direction):
        return product_schema_list.dump(utils.get_popular_products_by_category_id(category_id, direction)).data


class ParentCategoryBySubcategoryId(Resource):
    def get(self, category_id):
        return category_schema.dump(utils.get_parent_category_by_category_id(category_id)).data

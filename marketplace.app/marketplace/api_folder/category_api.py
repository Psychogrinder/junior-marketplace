from flask import request

import marketplace.api_folder.api_utils as utils
from flask_restful import Resource

from marketplace import cache
from marketplace.api_folder.schemas import category_schema_list, product_schema_list, category_schema


class CategoryRest(Resource):
    def get(self, slug):
        path = request.url
        if not cache.exists(path):
            category = category_schema.dump(utils.get_category_by_name(slug)).data
            return utils.cache_and_return(path, category), 200
        else:
            return utils.get_cached(path), 200


class BaseCategories(Resource):
    def get(self):
        path = request.url
        if not cache.exists(path):
            categories = category_schema_list.dump(utils.get_all_base_categories()).data
            return utils.cache_list_and_return(path, categories), 200
        else:
            return utils.get_cached_list(path)


class Subcategories(Resource):
    def get(self, category_id):
        path = request.url
        if not cache.exists(path):
            subcategories = category_schema_list.dump(utils.get_subcategories_by_category_id(category_id)).data
            return utils.cache_list_and_return(path, subcategories), 200
        else:
            return utils.get_cached_list(path), 200


class SubcategoriesBySlug(Resource):
    def get(self, category_slug):
        path = request.url
        if not cache.exists(path):
            subcategories = category_schema_list.dump(utils.get_subcategories_by_category_slug(category_slug)).data
            return utils.cache_list_and_return(path, subcategories), 200
        else:
            return utils.get_cached_list(path), 200


class ProductsByCategory(Resource):
    def get(self, category_id):
        path = request.url
        if not cache.exists(path):
            products = product_schema_list.dump(utils.get_products_by_category_id(category_id)).data
            return utils.cache_list_and_return(path, products), 200
        else:
            return utils.get_cached_list(path), 200


class PopularProductsByCategory(Resource):
    def get(self, category_id, direction):
        path = request.url
        if not cache.exists(path):
            products = product_schema_list.dump(utils.get_popular_products_by_category_id(category_id, direction)).data
            return utils.cache_list_and_return(path, products), 200
        else:
            return utils.get_cached_list(path), 200


class ParentCategoryBySubcategoryId(Resource):
    def get(self, category_id):
        path = request.url
        if not cache.exists(path):
            category = category_schema.dump(utils.get_parent_category_by_category_id(category_id)).data
            return utils.cache_and_return(path, category), 200
        else:
            return utils.get_cached(path), 200

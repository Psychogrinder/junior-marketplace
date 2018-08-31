from flask import request

import marketplace.api_folder.api_utils as utils
from flask_restful import Resource

from marketplace import cache
from marketplace.api_folder.schemas import category_schema_list, product_schema_list, category_schema


class CategoryRest(Resource):
    def get(self, slug):
        path = request.url
        category = utils.get_cached_json(path)
        if category is None:
            category = category_schema.dump(utils.get_category_by_name(slug)).data
            return utils.cache_json_and_get(path, category), 200
        else:
            return category, 200


class BaseCategories(Resource):
    def get(self):
        path = request.url
        categories = utils.get_cached_json(path)
        if categories is None:
            categories = category_schema_list.dump(utils.get_all_base_categories()).data
            return utils.cache_json_and_get(path, categories), 200
        else:
            return categories, 200


class Subcategories(Resource):
    def get(self, category_id):
        path = request.url
        subcategories = utils.get_cached_json(path)
        if subcategories is None:
            subcategories = category_schema_list.dump(utils.get_subcategories_by_category_id(category_id)).data
            return utils.cache_json_and_get(path, subcategories), 200
        else:
            return subcategories, 200


class SubcategoriesBySlug(Resource):
    def get(self, category_slug):
        path = request.url
        subcategories = utils.get_cached_json(path)
        if subcategories is None:
            subcategories = category_schema_list.dump(utils.get_subcategories_by_category_slug(category_slug)).data
            return utils.cache_json_and_get(path, subcategories), 200
        else:
            return subcategories, 200


class ProductsByCategory(Resource):
    def get(self, category_id):
        path = request.url
        products = utils.get_cached_json(path)
        if products is None:
            products = product_schema_list.dump(utils.get_products_by_category_id(category_id)).data
            return utils.cache_json_and_get(path, products), 200
        else:
            return products, 200


class PopularProductsByCategory(Resource):
    def get(self, category_id, direction):
        path = request.url
        products = utils.get_cached_json(path)
        if products is None:
            products = product_schema_list.dump(utils.get_popular_products_by_category_id(category_id, direction)).data
            return utils.cache_json_and_get(path, products), 200
        else:
            return products, 200


class ParentCategoryBySubcategoryId(Resource):
    def get(self, category_id):
        path = request.url
        category = utils.get_cached_json(path)
        if category is None:
            category = category_schema.dump(utils.get_parent_category_by_category_id(category_id)).data
            return utils.cache_json_and_get(path, category), 200
        else:
            return category, 200


class SubcategoryNamesByProducerName(Resource):
    def get(self, producer_name):
        return {'producer_name': producer_name,
                "category_names": utils.get_subcategory_names_by_producer_name(producer_name)}


class SubcategoryNamesByParentSlugAndProducerName(Resource):
    def get(self, parent_category_slug, producer_name):
        return utils.get_subcategory_names_by_parent_category_slug_and_producer_name(parent_category_slug,
                                                                                     producer_name)

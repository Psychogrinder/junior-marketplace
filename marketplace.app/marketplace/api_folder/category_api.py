from flask import request
import marketplace.api_folder.api_utils as utils
from flask_restful import Resource

from marketplace.api_folder.decorators import get_cache
from marketplace.api_folder.schemas import category_schema_list, product_schema_list, category_schema


class CategoryRest(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            category = category_schema.dump(utils.get_category_by_name(kwargs['slug'])).data
            return utils.cache_json_and_get(path, category), 200
        else:
            return cache, 200


class BaseCategories(Resource):

    @get_cache
    def get(self, path, cache):
        if cache is None:
            categories = category_schema_list.dump(utils.get_all_base_categories()).data
            return utils.cache_json_and_get(path, categories), 200
        else:
            return cache, 200


class Subcategories(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            subcategories = category_schema_list.dump(
                utils.get_subcategories_by_category_id(kwargs['category_id'])).data
            return utils.cache_json_and_get(path, subcategories), 200
        else:
            return cache, 200


class SubcategoriesBySlug(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            subcategories = category_schema_list.dump(
                utils.get_subcategories_by_category_slug(kwargs['category_slug'])).data
            return utils.cache_json_and_get(path, subcategories), 200
        else:
            return cache, 200


class ProductsByCategory(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            products = product_schema_list.dump(utils.get_products_by_category_id(kwargs['category_id'])).data
            return utils.cache_json_and_get(path, products), 200
        else:
            return cache, 200


class PopularProductsByCategory(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            products = product_schema_list.dump(
                utils.get_popular_products_by_category_id(kwargs['category_id'], kwargs['direction'])).data
            return utils.cache_json_and_get(path, products), 200
        else:
            return cache, 200


class ParentCategoryBySubcategoryId(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            category = category_schema.dump(utils.get_parent_category_by_category_id(kwargs['category_id'])).data
            return utils.cache_json_and_get(path, category), 200
        else:
            return cache, 200


class SubcategoryNamesByProducerName(Resource):
    def get(self, producer_name):
        return {'producer_name': producer_name,
                "category_names": utils.get_subcategory_names_by_producer_name(producer_name)}


class SubcategoryNamesByParentSlugAndProducerName(Resource):
    def get(self, parent_category_slug, producer_name):
        return utils.get_subcategory_names_by_parent_category_slug_and_producer_name(parent_category_slug,
                                                                                     producer_name)

from marketplace.api_folder.utils import category_utils
from marketplace.api_folder.utils import product_utils
from flask_restful import Resource
from marketplace.api_folder.decorators import get_cache
from marketplace.api_folder.schemas import category_schema_list, product_schema_list, category_schema
from marketplace.api_folder.utils import caching_utils


class CategoryRest(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            category = category_schema.dump(category_utils.get_category_by_name(kwargs['slug'])).data
            return caching_utils.cache_json_and_get(path, category), 200
        else:
            return cache, 200


class BaseCategories(Resource):

    @get_cache
    def get(self, path, cache):
        if cache is None:
            categories = category_schema_list.dump(category_utils.get_all_base_categories()).data
            return caching_utils.cache_json_and_get(path, categories), 200
        else:
            return cache, 200


class Subcategories(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            subcategories = category_schema_list.dump(
                category_utils.get_subcategories_by_category_id(kwargs['category_id'])).data
            return caching_utils.cache_json_and_get(path, subcategories), 200
        else:
            return cache, 200


class SubcategoriesBySlug(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            subcategories = category_schema_list.dump(
                category_utils.get_subcategories_by_category_slug(kwargs['category_slug'])).data
            return caching_utils.cache_json_and_get(path, subcategories), 200
        else:
            return cache, 200


class ProductsByCategory(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            products = product_schema_list.dump(product_utils.get_products_by_category_id(kwargs['category_id'])).data
            return caching_utils.cache_json_and_get(path, products), 200
        else:
            return cache, 200


class PopularProductsByCategory(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            products = product_schema_list.dump(
                product_utils.get_popular_products_by_category_id(kwargs['category_id'], kwargs['direction'])).data
            return caching_utils.cache_json_and_get(path, products), 200
        else:
            return cache, 200


class ParentCategoryBySubcategoryId(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            category = category_schema.dump(
                category_utils.get_parent_category_by_category_id(kwargs['category_id'])).data
            return caching_utils.cache_json_and_get(path, category), 200
        else:
            return cache, 200


# Не было такое функции get_subcategory_names_by_producer_name
class SubcategoryNamesByProducerName(Resource):
    def get(self, producer_name):
        return {'producer_name': producer_name,
                "category_names": category_utils.get_subcategory_names_by_producer_name(producer_name)}


class SubcategoryNamesByParentSlugAndProducerName(Resource):
    def get(self, parent_category_slug, producer_name):
        return category_utils.get_subcategory_names_by_parent_category_slug_and_producer_name(parent_category_slug,
                                                                                              producer_name)

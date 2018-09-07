from flask import request, redirect, url_for
from flask_restful import Resource, reqparse
from marketplace.api_folder.utils import product_utils
from marketplace.api_folder.utils import cart_utils
from marketplace.api_folder.schemas import product_schema_list, product_schema
from marketplace.api_folder.utils import caching_utils
from marketplace.api_folder.utils.caching_utils import get_cache

product_args = ['price', 'name', 'quantity', 'producer_id', 'category_id', 'measurement_unit', 'weight', 'description']
parser = reqparse.RequestParser()

for arg in product_args:
    parser.add_argument(arg)

search_parser = reqparse.RequestParser()
search_parser.add_argument(
    'find', type=str, location='args', required=True
)


class GlobalProducts(Resource):

    @get_cache
    def get(self, path, cache):
        if cache is None:
            products = product_schema_list.dump(product_utils.get_all_products()).data
            return caching_utils.cache_json_and_get(path=path, response=products), 200
        else:
            return cache, 200

    def post(self):
        args = parser.parse_args()
        if product_utils.producer_has_product_with_such_name(args):
            return {'message': f'У этого производителя уже есть товар с именем {args["name"]}'}
        return product_schema.dump(product_utils.post_product(args)).data, 201


class ProductRest(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            product = product_schema.dump(product_utils.get_product_by_id(kwargs['product_id'])).data
            return caching_utils.cache_json_and_get(path=path, response=product), 200
        else:
            return cache, 200

    def put(self, product_id):
        args = parser.parse_args()
        return product_schema.dump(product_utils.put_product(args, product_id)).data, 201

    def delete(self, product_id):
        return product_utils.delete_product_by_id(product_id), 201


class PopularProducts(Resource):

    @get_cache
    def get(self, path, cache):
        if cache is None:
            products = product_schema_list.dump(product_utils.get_popular_products()).data
            return caching_utils.cache_json_and_get(path=path, response=products), 200
        else:
            return cache, 200


class ProductsByPrice(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            products = product_schema_list.dump(
                product_utils.get_products_by_category_id_sorted_by_price(kwargs['category_id'],
                                                                          kwargs['direction'])).data
            return caching_utils.cache_json_and_get(path=path, response=products), 200
        else:
            return cache, 200


class UploadImageProduct(Resource):
    def post(self, product_id):
        return product_utils.upload_product_image(product_id, request.files)


class ProductsInCart(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            products = product_schema_list.dump(
                cart_utils.get_products_from_cart(cart_utils.get_cart_by_consumer_id(kwargs['consumer_id']).items)).data
            return caching_utils.cache_json_and_get(path=path, response=products), 200
        else:
            return cache, 200


class ProductSearchByParams(Resource):

    @get_cache
    def get(self, path, cache):
        if cache is None:
            args = search_parser.parse_args()
            search_query = '&'.join(args['find'].split(' '))
            result = product_utils.search_products_by_param(search_query)
            if result is None:
                return {}, 400
            return caching_utils.cache_json_and_get(path=path, response=product_schema_list.dump(result).data), 200
        else:
            return cache


product_args = ['price', 'popularity', 'category_name', 'producer_name', 'in_stock']
filter_parser = reqparse.RequestParser()

for arg in product_args:
    filter_parser.add_argument(arg)


class ProductsSortedAndFiltered(Resource):
    def post(self):
        args = filter_parser.parse_args()
        # return product_schema_list.dump(utils.get_sorted_and_filtered_products(args)).data
        return product_utils.get_sorted_and_filtered_products(args)

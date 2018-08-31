from flask import request
from flask_restful import Resource, reqparse
import marketplace.api_folder.api_utils as utils
from marketplace import cache
from marketplace.api_folder.schemas import product_schema_list, product_schema

product_args = ['price', 'name', 'quantity', 'producer_id', 'category_id', 'measurement_unit', 'weight', 'description']
parser = reqparse.RequestParser()

for arg in product_args:
    parser.add_argument(arg)

search_parser = reqparse.RequestParser()
search_parser.add_argument(
    'find', type=str, location='args', required=True
)


class GlobalProducts(Resource):
    def get(self):
        path = request.url
        products = utils.get_cached_json(path)
        if products is None:
            products = product_schema_list.dump(utils.get_all_products()).data
            return utils.cache_json_and_get(path, products), 200
        else:
            return products, 200

    def post(self):
        args = parser.parse_args()
        if utils.producer_has_product_with_such_name(args):
            return {'message': f'У этого производителя уже есть товар с именем {args["name"]}'}
        return product_schema.dump(utils.post_product(args)).data, 201


class ProductRest(Resource):
    def get(self, product_id):
        path = request.url
        product = utils.get_cached_json(path)
        if product is None:
            product = product_schema.dump(utils.get_product_by_id(product_id)).data
            return utils.cache_json_and_get(path, product), 200
        else:
            return product, 200

    def put(self, product_id):
        args = parser.parse_args()
        return product_schema.dump(utils.put_product(args, product_id)).data, 201

    def delete(self, product_id):
        return utils.delete_product_by_id(product_id), 201


class PopularProducts(Resource):
    def get(self):
        path = request.url
        products = utils.get_cached_json(path)
        if products is None:
            products = product_schema_list.dump(utils.get_popular_products()).data
            return utils.cache_json_and_get(path, products), 200
        else:
            return products, 200


class ProductsByPrice(Resource):
    def get(self, category_id, direction):
        path = request.url
        products = utils.get_cached_json(path)
        if products is None:
            products = product_schema_list.dump(
                utils.get_products_by_category_id_sorted_by_price(category_id, direction)).data
            return utils.cache_json_and_get(path, products), 200
        else:
            return products, 200


class UploadImageProduct(Resource):
    def post(self, product_id):
        return utils.upload_product_image(product_id, request.files), 201


class ProductsInCart(Resource):
    def get(self, consumer_id):
        path = request.url
        products = utils.get_cached_json(path)
        if products is None:
            products = product_schema_list.dump(
                utils.get_products_from_cart(utils.get_cart_by_consumer_id(consumer_id).items)).data
            return utils.cache_json_and_get(path, products), 200
        else:
            return products, 200


class ProductSearchByParams(Resource):
    def get(self):
        path = request.url
        result = utils.get_cached_json(path)
        if result is None:
            args = search_parser.parse_args()
            search_query = '&'.join(args['find'].split(' '))
            result = utils.search_products_by_param(search_query)
            if result is None:
                return {}, 400
            return utils.cache_json_and_get(path, product_schema_list.dump(result).data), 200
        else:
            return result


product_args = ['price', 'popularity', 'category_name', 'producer_name', 'in_stock']
filter_parser = reqparse.RequestParser()

for arg in product_args:
    filter_parser.add_argument(arg)


class ProductsSortedAndFiltered(Resource):
    def post(self):
        args = filter_parser.parse_args()
        # return product_schema_list.dump(utils.get_sorted_and_filtered_products(args)).data
        return utils.get_sorted_and_filtered_products(args)

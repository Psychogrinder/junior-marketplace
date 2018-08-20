from flask_restful import Resource, reqparse
import marketplace.api.api_utils as utils

product_args = ['price', 'name', 'quantity', 'producer_id', 'category_id', 'measurement_unit', 'weight', 'description']
parser = reqparse.RequestParser()

for arg in product_args:
    parser.add_argument(arg)


class GlobalProducts(Resource):
    def get(self):
        return utils.get_all_products()

    def post(self):
        args = parser.parse_args()
        return utils.post_product(args), 201


class ProductRest(Resource):
    def get(self, product_id):
        return utils.get_product_by_id(product_id)

    def put(self, product_id):
        args = parser.parse_args()
        return utils.put_product(args, product_id), 201

    def delete(self, product_id):
        return utils.delete_product_by_id(product_id), 201


class PopularProducts(Resource):
    def get(self):
        return utils.get_popular_products()

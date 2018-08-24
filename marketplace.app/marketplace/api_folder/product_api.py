from flask import request
from flask_restful import Resource, reqparse
import marketplace.api_folder.api_utils as utils
from marketplace.api_folder.schemas import product_schema_list, product_schema

product_args = ['price', 'name', 'quantity', 'producer_id', 'category_id', 'measurement_unit', 'weight', 'description']
parser = reqparse.RequestParser()

for arg in product_args:
    parser.add_argument(arg)


class GlobalProducts(Resource):
    def get(self):
        return product_schema_list.dump(utils.get_all_products()).data

    def post(self):
        args = parser.parse_args()
        if utils.producer_has_product_with_such_name(args):
            return {'message': f'У этого производителя уже есть товар с именем {args["name"]}'}
        return product_schema.dump(utils.post_product(args)).data, 201


class ProductRest(Resource):
    def get(self, product_id):
        return product_schema.dump(utils.get_product_by_id(product_id)).data

    def put(self, product_id):
        args = parser.parse_args()
        return product_schema.dump(utils.put_product(args, product_id)).data, 201

    def delete(self, product_id):
        return utils.delete_product_by_id(product_id), 201


class PopularProducts(Resource):
    def get(self):
        return product_schema_list.dump(utils.get_popular_products()).data


class UploadImageProduct(Resource):
    def post(self, product_id):
        return utils.upload_product_image(product_id, request.files), 201

from flask import request
from flask_restful import Resource, reqparse
import marketplace.api_folder.api_utils as utils
from marketplace.api_folder.schemas import producer_schema_list, producer_schema, order_schema_list, product_schema_list

producer_args = ['email', 'name', 'password', 'person_to_contact', 'description', 'phone_number', 'address']

parser = reqparse.RequestParser()

for arg in producer_args:
    parser.add_argument(arg)


class GlobalProducers(Resource):
    def get(self):
        response = dict()
        page_number = request.args.get('page', type=int, default=1)
        page = utils.get_all_producers(page_number)
        response['meta'] = utils.get_meta_from_page(page_number, page)
        response['body'] = product_schema_list.dump(page.items).data
        return response, 200

    def post(self):
        args = parser.parse_args()
        return producer_schema.dump(utils.post_producer(args)).data, 201


class ProducerRest(Resource):

    def get(self, producer_id):
        return producer_schema.dump(utils.get_producer_by_id(producer_id)).data

    def put(self, producer_id):
        args = parser.parse_args()
        return producer_schema.dump(utils.put_producer(args, producer_id)).data, 201

    def delete(self, producer_id):
        return utils.delete_producer_by_id(producer_id), 201


class ProducerOrders(Resource):
    def get(self, producer_id):
        response = dict()
        page_number = request.args.get('page', type=int, default=1)
        page = utils.get_orders_by_producer_id(producer_id, page_number)
        response['meta'] = utils.get_meta_from_page(page_number, page)
        response['body'] = order_schema_list.dump(page.items).data
        return response, 200


class ProductsByProducer(Resource):
    def get(self, producer_id):
        response = dict()
        page_number = request.args.get('page', type=int, default=1)
        page = utils.get_products_by_producer_id(producer_id, page_number)
        response['meta'] = utils.get_meta_from_page(page_number, page)
        response['body'] = product_schema_list.dump(page.items).data
        return response, 200


class UploadImageProducer(Resource):
    def post(self, producer_id):
        return utils.upload_producer_image(producer_id, request.files), 201

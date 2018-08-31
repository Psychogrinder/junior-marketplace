from flask import request
from flask_restful import Resource, reqparse
import marketplace.api_folder.api_utils as utils
from marketplace import cache
from marketplace.api_folder.schemas import producer_schema_list, producer_schema, order_schema_list, product_schema_list

producer_args = ['email', 'name', 'password', 'person_to_contact', 'description', 'phone_number', 'address']

parser = reqparse.RequestParser()

for arg in producer_args:
    parser.add_argument(arg)


class GlobalProducers(Resource):
    def get(self):
        path = request.url
        producers = utils.get_cached_json(path)
        if producers is None:
            producers = producer_schema_list.dump(utils.get_all_producers()).data
            return utils.cache_json_and_get(path, producers), 200
        else:
            return producers, 200

    def post(self):
        args = parser.parse_args()
        return producer_schema.dump(utils.post_producer(args)).data, 201


class ProducerRest(Resource):

    def get(self, producer_id):
        path = request.url
        producer = utils.get_cached_json(path)
        if producer is None:
            producer = producer_schema.dump(utils.get_producer_by_id(producer_id)).data
            return utils.cache_json_and_get(path, producer), 200
        else:
            return producer, 200

    def put(self, producer_id):
        args = parser.parse_args()
        return producer_schema.dump(utils.put_producer(args, producer_id)).data, 201

    def delete(self, producer_id):
        return utils.delete_producer_by_id(producer_id), 201


class ProducerOrders(Resource):
    def get(self, producer_id):
        path = request.url
        orders = utils.get_cached_json(path)
        if orders is None:
            orders = order_schema_list.dump(utils.get_orders_by_producer_id(producer_id)).data
            return utils.cache_json_and_get(path, orders), 200
        else:
            return orders, 200


class ProductsByProducer(Resource):
    def get(self, producer_id):
        path = request.url
        products = utils.get_cached_json(path)
        if products is None:
            products = product_schema_list.dump(utils.get_products_by_producer_id(producer_id)).data
            return utils.cache_json_and_get(path, products), 200
        else:
            return products, 200


class UploadImageProducer(Resource):
    def post(self, producer_id):
        return utils.upload_producer_image(producer_id, request.files), 201


class ProducerNamesByCategoryName(Resource):
    def get(self, category_name):
        return utils.get_producer_names_by_category_name(category_name), 200

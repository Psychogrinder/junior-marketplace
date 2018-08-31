from flask import request
from flask_restful import Resource, reqparse
import marketplace.api_folder.api_utils as utils
from marketplace.api_folder.decorators import get_cache
from marketplace.api_folder.schemas import producer_schema_list, producer_schema, order_schema_list, product_schema_list

producer_args = ['email', 'name', 'password', 'person_to_contact', 'description', 'phone_number', 'address']

parser = reqparse.RequestParser()

for arg in producer_args:
    parser.add_argument(arg)


class GlobalProducers(Resource):

    @get_cache
    def get(self, path, cache):
        if cache is None:
            producers = producer_schema_list.dump(utils.get_all_producers()).data
            return utils.cache_json_and_get(path, producers), 200
        else:
            return cache, 200

    def post(self):
        args = parser.parse_args()
        return producer_schema.dump(utils.post_producer(args)).data, 201


class ProducerRest(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            producer = producer_schema.dump(utils.get_producer_by_id(kwargs['producer_id'])).data
            return utils.cache_json_and_get(path, producer), 200
        else:
            return cache, 200

    def put(self, producer_id):
        args = parser.parse_args()
        return producer_schema.dump(utils.put_producer(args, producer_id)).data, 201

    def delete(self, producer_id):
        return utils.delete_producer_by_id(producer_id), 201


class ProducerOrders(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            orders = order_schema_list.dump(utils.get_orders_by_producer_id(kwargs['producer_id'])).data
            return utils.cache_json_and_get(path, orders), 200
        else:
            return cache, 200


class ProductsByProducer(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            products = product_schema_list.dump(utils.get_products_by_producer_id(kwargs['producer_id'])).data
            return utils.cache_json_and_get(path, products), 200
        else:
            return cache, 200


class UploadImageProducer(Resource):
    def post(self, producer_id):
        return utils.upload_producer_image(producer_id, request.files), 201


class ProducerNamesByCategoryName(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            names = utils.get_producer_names_by_category_name(kwargs['category_name'])
            return utils.cache_json_and_get(path, names), 200
        else:
            return cache, 200

from marketplace import cache
from flask import request
from flask_restful import Resource, reqparse
import marketplace.api_folder.api_utils as utils
from marketplace.api_folder.schemas import (
    consumer_schema_list,
    consumer_schema,
    order_schema_list)

consumer_args = ['first_name', 'last_name', 'email', 'password', 'phone_number', 'category_id', 'address', 'photo_url',
                 'patronymic']
parser = reqparse.RequestParser()

for arg in consumer_args:
    parser.add_argument(arg)


class GlobalConsumers(Resource):
    def get(self):
        path = request.url
        if not cache.exists(path):
            consumers = consumer_schema_list.dump(utils.get_all_consumers()).data
            return utils.cache_list_and_return(path, consumers), 200
        else:
            return utils.get_cached_list(path), 200

    def post(self):
        args = parser.parse_args()
        return consumer_schema.dump(utils.post_consumer(args)).data, 201


class ConsumerRest(Resource):
    def get(self, consumer_id):
        path = request.url
        if not cache.exists(path):
            consumer = consumer_schema.dump(utils.get_consumer_by_id(consumer_id)).data
            return utils.cache_and_return(path, consumer), 200
        else:
            return utils.get_cached(path), 200

    def put(self, consumer_id):
        args = parser.parse_args()
        return consumer_schema.dump(utils.put_consumer(args, consumer_id)).data, 201

    def delete(self, consumer_id):
        return utils.delete_consumer_by_id(consumer_id), 201


class ConsumerOrders(Resource):

    def get(self, consumer_id):
        path = request.url
        if not cache.exists(path):
            orders = order_schema_list.dump(utils.get_orders_by_consumer_id(consumer_id)).data
            return utils.cache_list_and_return(path, orders), 200
        else:
            return utils.get_cached_list(path), 200


class UploadImageConsumer(Resource):
    def post(self, consumer_id):
        return utils.upload_consumer_image(consumer_id, request.files), 201

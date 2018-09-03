from flask import request
from flask_restful import Resource, reqparse
import marketplace.api_folder.api_utils as utils
from marketplace.api_folder.decorators import get_cache
from marketplace.api_folder.repositories import consumer_repository
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

    @get_cache
    def get(self, path, cache):
        if cache is None:
            consumers = consumer_schema_list.dump(consumer_repository.get_by_id()).data
            return utils.cache_json_and_get(path, consumers), 200
        else:
            return cache, 200

    def post(self):
        args = parser.parse_args()
        return consumer_schema.dump(consumer_repository.post(args)).data, 201


class ConsumerRest(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            consumer = consumer_schema.dump(consumer_repository.get_by_id(kwargs['consumer_id'])).data
            return utils.cache_json_and_get(path, consumer), 200
        else:
            return cache, 200

    def put(self, consumer_id):
        args = parser.parse_args()
        return consumer_schema.dump(consumer_repository.put(args, consumer_id)).data, 201

    def delete(self, consumer_id):
        return consumer_repository.delete_by_id(consumer_id), 201


class ConsumerOrders(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            orders = order_schema_list.dump(utils.get_orders_by_consumer_id(kwargs['consumer_id'])).data
            return utils.cache_json_and_get(path, orders), 200
        else:
            return cache, 200


class UploadImageConsumer(Resource):
    def post(self, consumer_id):
        return utils.upload_consumer_image(consumer_id, request.files), 201

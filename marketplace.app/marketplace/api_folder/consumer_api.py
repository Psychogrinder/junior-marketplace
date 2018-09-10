from flask import request
from flask_restful import Resource, reqparse
from marketplace.api_folder.utils import consumer_utils, comment_utils, pagination_utils
from marketplace.api_folder.utils import order_utils
from marketplace.api_folder.schemas import (
    consumer_schema_list,
    consumer_schema,
    order_schema_list, comment_schema_list)
from marketplace.api_folder.utils import caching_utils
from marketplace.api_folder.utils.caching_utils import get_cache
from flask_httpauth import HTTPBasicAuth

from marketplace.api_folder.utils.login_utils import login_as_admin_required, account_access_required

consumer_args = ['first_name', 'last_name', 'email', 'password', 'phone_number', 'category_id', 'address', 'photo_url',
                 'patronymic']
parser = reqparse.RequestParser()

for arg in consumer_args:
    parser.add_argument(arg)


class GlobalConsumers(Resource):

    @login_as_admin_required
    @get_cache
    def get(self, path, cache):
        if cache is None:
            consumers = consumer_schema_list.dump(consumer_utils.get_all_consumers()).data
            return caching_utils.cache_json_and_get(path=path, response=consumers), 200
        else:
            return cache, 200

    def post(self):
        args = parser.parse_args()
        return consumer_schema.dump(consumer_utils.post_consumer(args)).data, 201


class ConsumerRest(Resource):

    @account_access_required
    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            consumer = consumer_schema.dump(consumer_utils.get_consumer_by_id(kwargs['consumer_id'])).data
            return caching_utils.cache_json_and_get(path=path, response=consumer), 200
        else:
            return cache, 200

    @account_access_required
    def put(self, **kwargs):
        args = parser.parse_args()
        return consumer_schema.dump(consumer_utils.put_consumer(args, kwargs['consumer_id'])).data, 201

    @account_access_required
    def delete(self, **kwargs):
        return consumer_utils.delete_consumer_by_id(kwargs['consumer_id']), 201


class ConsumerOrders(Resource):

    @account_access_required
    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            orders = order_schema_list.dump(order_utils.get_orders_by_consumer_id(kwargs['consumer_id'])).data
            return caching_utils.cache_json_and_get(path=path, response=orders), 200
        else:
            return cache, 200


class ConsumerComments(Resource):
    @account_access_required
    @get_cache
    def get(self, path, cache, **kwargs):
        response = dict()
        page_number = pagination_utils.get_page_number()
        if cache is None or 'meta' not in kwargs:
            comments_page = comment_utils.get_comments_by_consumer_id(kwargs['consumer_id'], page_number)
            response['meta'] = caching_utils.cache_json_and_get(path='{}/meta'.format(path),
                                                                response=pagination_utils.get_meta_from_page(
                                                                    page_number, comments_page))
            response['body'] = caching_utils.cache_json_and_get(path=path, response=comment_schema_list.dump(
                comments_page.items).data)
        else:
            response['meta'] = kwargs['meta']
            response['body'] = cache
        return response, 200


class UploadImageConsumer(Resource):
    @account_access_required
    def post(self, **kwargs):
        return consumer_utils.upload_consumer_image(kwargs['consumer_id'], request.files), 201

from flask import request
from flask_restful import Resource, reqparse
import marketplace.api_folder.api_utils as utils
from marketplace.api_folder.decorators import get_cache
from marketplace.api_folder.schemas import order_schema_list, order_schema

order_args = ['orders', 'delivery_address', 'phone', 'email', 'consumer_id', 'status', 'total_cost', 'first_name',
              'last_name']
parser = reqparse.RequestParser()

for arg in order_args:
    parser.add_argument(arg)


class GlobalOrders(Resource):

    @get_cache
    def get(self, path, cache):
        if cache is None:
            orders = order_schema_list.dump(utils.get_all_orders()).data
            return utils.cache_json_and_get(path, orders), 200
        else:
            return cache, 200

    def post(self):
        args = parser.parse_args()
        utils.decrease_products_quantity_and_increase_times_ordered(args['consumer_id'])
        utils.post_orders(args)
        return "Заказ был успешно оформлен", 201


class Orders(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            order = order_schema.dump(utils.get_order_by_id(kwargs['order_id'])).data
            return utils.cache_json_and_get(path, order), 200
        else:
            return cache, 200

    def put(self, order_id):
        args = parser.parse_args()
        return order_schema.dump(utils.put_order(args, order_id)).data, 201

    def delete(self, order_id):
        utils.increase_products_quantity_and_decrease_times_ordered(order_id)
        return utils.delete_order_by_id(order_id), 202


class UnprocessedOrdersByProducerId(Resource):
    def get(self, producer_id):
        return {"quantity": utils.get_number_of_unprocessed_orders_by_producer_id(producer_id)}, 200

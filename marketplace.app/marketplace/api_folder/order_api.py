from flask_login import login_required, current_user
from flask_restful import Resource, reqparse
from marketplace.api_folder.utils import order_utils
from marketplace.api_folder.schemas import order_schema_list, order_schema
from marketplace.api_folder.utils import caching_utils
import marketplace.api_folder.utils.cart_utils as cart_utils
from marketplace.api_folder.utils.caching_utils import get_cache
from marketplace.api_folder.utils.login_utils import account_access_required

order_args = ['orders', 'delivery_address', 'phone', 'email', 'consumer_id', 'status', 'total_cost', 'first_name',
              'last_name']
parser = reqparse.RequestParser()

for arg in order_args:
    parser.add_argument(arg)


class GlobalOrders(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            orders = order_schema_list.dump(order_utils.get_all_orders()).data
            return caching_utils.cache_json_and_get(path=path, response=orders), 200
        else:
            return cache, 200

    @login_required
    def post(self, **kwargs):
        args = parser.parse_args()
        cart_utils.decrease_products_quantity_and_increase_times_ordered(current_user.id)
        cart_utils.post_orders(args)
        return "Заказ был успешно оформлен", 201


class Orders(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            order = order_schema.dump(order_utils.get_order_by_id(kwargs['order_id'])).data
            return caching_utils.cache_json_and_get(path=path, response=order), 200
        else:
            return cache, 200

    def put(self, order_id):
        args = parser.parse_args()
        return order_schema.dump(order_utils.put_order(args, order_id)).data, 201

    def delete(self, order_id):
        cart_utils.increase_products_quantity_and_decrease_times_ordered(order_id)
        return order_utils.delete_order_by_id(order_id), 202


class UnprocessedOrdersByProducerId(Resource):
    @account_access_required
    def get(self, **kwargs):
        return {"quantity": order_utils.get_number_of_unprocessed_orders_by_producer_id(kwargs['producer_id'])}, 200


filtered_orders_args = ['producer_id', 'order_status']
filtered_orders_parser = reqparse.RequestParser()
for arg in filtered_orders_args:
    filtered_orders_parser.add_argument(arg)


class FilteredOrdersByProducerId(Resource):
    def post(self):
        args = filtered_orders_parser.parse_args()
        return order_utils.get_filtered_orders(args), 200


consumer_order_parser = reqparse.RequestParser()
consumer_order_parser.add_argument('page')
consumer_order_parser.add_argument('consumer_id')


class FormattedConsumerOrders(Resource):
    def post(self):
        args = consumer_order_parser.parse_args()
        return order_utils.get_formatted_orders_by_consumer_id(args['consumer_id'], int(args['page']))

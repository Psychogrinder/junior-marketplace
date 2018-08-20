from flask_restful import Resource, reqparse
import marketplace.api.api_utils as utils
from marketplace.api.schemas import order_schema_list, order_schema

order_args = ['total_cost', 'order_items_json', 'delivery_method', 'delivery_address', 'consumer_phone',
              'consumer_email', 'consumer_id', 'producer_id', 'status']
parser = reqparse.RequestParser()

for arg in order_args:
    parser.add_argument(arg)


class GlobalOrders(Resource):

    def get(self):
        return order_schema_list.dump(utils.get_all_orders()).data

    def post(self):
        args = parser.parse_args()
        return order_schema.dump(utils.post_order(args)).data, 201


class Orders(Resource):
    def get(self, order_id):
        return order_schema.dump(utils.get_order_by_id(order_id)).data

    def put(self, order_id):
        args = parser.parse_args()
        return order_schema.dump(utils.put_order(args, order_id)).data, 201

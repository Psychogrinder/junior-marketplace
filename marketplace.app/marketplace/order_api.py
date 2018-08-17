from flask_restful import Resource, reqparse
import marketplace.api_utils as utils

order_args = ['total_cost', 'order_items_json', 'delivery_method', 'delivery_address', 'consumer_phone',
              'consumer_email', 'consumer_id', 'producer_id', 'status']
parser = reqparse.RequestParser()

for arg in order_args:
    parser.add_argument(arg)


class GlobalOrders(Resource):

    def get(self):
        return utils.get_all_orders()

    def post(self):
        args = parser.parse_args()
        return utils.post_order(args), 201


class Orders(Resource):
    def get(self, order_id):
        return utils.get_order_by_id(order_id)

    def put(self, order_id):
        args = parser.parse_args()
        return utils.put_order(args, order_id), 201




from flask_restful import Resource, reqparse
import marketplace.api_utils as utils

consumer_args = ['full_name', 'email', 'phone', 'category_id', 'address', 'photo_url', 'orders']
parser = reqparse.RequestParser()

for arg in consumer_args:
    parser.add_argument(arg)


class GlobalConsumers(Resource):
    def get(self):
        return utils.get_all_consumers()

    def post(self):
        args = parser.parse_args()
        return utils.post_consumer(args), 201


class ConsumerRest(Resource):
    def get(self, consumer_id):
        return utils.get_consumer_by_id(consumer_id)

    def put(self, consumer_id):
        args = parser.parse_args()
        return utils.put_consumer(args, consumer_id), 201

    def delete(self, consumer_id):
        return utils.delete_consumer_by_id(consumer_id), 201


class ConsumerOrders(Resource):

    def get(self, consumer_id):
        return utils.get_orders_by_consumer_id(consumer_id)



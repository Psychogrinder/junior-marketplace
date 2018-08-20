from flask_restful import Resource, reqparse
import marketplace.api_folder.api_utils as utils
from marketplace.api_folder.schemas import consumer_schema_list, consumer_schema, order_schema

consumer_args = ['first_name', 'last_name', 'email', 'password', 'phone', 'category_id', 'address', 'photo_url']
parser = reqparse.RequestParser()

for arg in consumer_args:
    parser.add_argument(arg)


class GlobalConsumers(Resource):
    def get(self):
        return consumer_schema_list.dump(utils.get_all_consumers())

    def post(self):
        args = parser.parse_args()
        return consumer_schema.dump(utils.post_consumer(args)).data, 201


class ConsumerRest(Resource):
    def get(self, consumer_id):
        return consumer_schema.dump(utils.get_consumer_by_id(consumer_id)).data

    def put(self, consumer_id):
        args = parser.parse_args()
        return consumer_schema.dump(utils.put_consumer(args, consumer_id)).data, 201

    def delete(self, consumer_id):
        return utils.delete_consumer_by_id(consumer_id), 201


class ConsumerOrders(Resource):

    def get(self, consumer_id):
        return order_schema.dump(utils.get_orders_by_consumer_id(consumer_id)).data

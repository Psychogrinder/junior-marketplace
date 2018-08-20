from flask_restful import Resource, reqparse
import marketplace.api.api_utils as utils

producer_args = ['email', 'name', 'password', 'person_to_contact', 'description', 'phone_number', 'address']

parser = reqparse.RequestParser()

for arg in producer_args:
    parser.add_argument(arg)


class GlobalProducers(Resource):
    def get(self):
        return utils.get_all_producers()

    def post(self):
        args = parser.parse_args()
        return utils.post_producer(args), 201


class ProducerRest(Resource):

    def get(self, producer_id):
        return utils.get_producer_by_id(producer_id)

    def put(self, producer_id):
        args = parser.parse_args()
        return utils.put_producer(args, producer_id), 201

    def delete(self, producer_id):
        return utils.delete_producer_by_id(producer_id), 201


class ProducerOrders(Resource):
    def get(self, producer_id):
        return utils.get_orders_by_producer_id(producer_id)


class ProductsByProducer(Resource):
    def get(self, producer_id):
        return utils.get_products_by_producer_id(producer_id)

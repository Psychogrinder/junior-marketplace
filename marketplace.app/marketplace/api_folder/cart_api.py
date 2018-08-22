from flask_restful import Resource, reqparse
import marketplace.api_folder.api_utils as utils
from marketplace.api_folder.schemas import basket_schema

basket_args = ['product_id', 'quantity']
parser = reqparse.RequestParser()

for arg in basket_args:
    parser.add_argument(arg)


class GlobalBasket(Resource):
    def get(self, consumer_id):
        return basket_schema.dump(utils.get_basket_by_consumer_id(consumer_id)).data

    def post(self, consumer_id):
        args = parser.parse_args()
        return basket_schema.dump(utils.post_item_to_basket_by_consumer_id(args, consumer_id)).data, 201

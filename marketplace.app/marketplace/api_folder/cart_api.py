from flask_restful import Resource, reqparse
import marketplace.api_folder.utils.cart_utils as cart_utils
from marketplace.api_folder.schemas import cart_schema
from marketplace.api_folder.utils.caching_utils import cache_json_and_get, get_cache
from marketplace.api_folder.utils.login_utils import account_access_required

cart_args = ['mode', 'product_id', 'quantity']
parser = reqparse.RequestParser()

for arg in cart_args:
    parser.add_argument(arg)


class GlobalCart(Resource):

    @account_access_required
    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            cart = cart_schema.dump(cart_utils.get_cart_by_consumer_id(kwargs['consumer_id'])).data
            return cache_json_and_get(path=path, response=cart), 200
        else:
            return cache, 200

    @account_access_required
    def post(self, **kwargs):
        args = parser.parse_args()
        if args['mode'] == 'remove':
            return cart_schema.dump(
                cart_utils.remove_item_from_cart_by_consumer_id(args, kwargs['consumer_id'])).data, 201
        else:
            return cart_schema.dump(cart_utils.post_item_to_cart_by_consumer_id(args, kwargs['consumer_id'])).data, 201

    @account_access_required
    def delete(self, **kwargs):
        return cart_utils.clear_cart_by_consumer_id(kwargs['consumer_id']), 201


class NumberOfProductsInCart(Resource):
    @account_access_required
    def get(self, **kwargs):
        return {"number_of_products": cart_utils.get_number_of_products_in_cart(kwargs['consumer_id'])}

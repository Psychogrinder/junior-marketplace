from flask import request
from flask_restful import Resource, reqparse
from flask_login import current_user
from marketplace import db
from marketplace.api_folder.utils import producer_utils
from marketplace.api_folder.utils import order_utils
from marketplace.api_folder.utils import product_utils
from marketplace.api_folder.schemas import producer_schema_list, producer_schema, order_schema_list, product_schema_list
from marketplace.api_folder.utils import caching_utils
from marketplace.api_folder.utils.caching_utils import get_cache
from marketplace.api_folder.utils.login_utils import account_access_required
from marketplace.trello_integrations import create_new_board, commit_change

producer_args = ['email', 'name', 'password', 'person_to_contact', 'description', 'phone_number', 'address']

parser = reqparse.RequestParser()

for arg in producer_args:
    parser.add_argument(arg)


class GlobalProducers(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            producers = producer_schema_list.dump(producer_utils.get_all_producers()).data
            return caching_utils.cache_json_and_get(path=path, response=producers), 200
        else:
            return cache, 200

    def post(self):
        args = parser.parse_args()
        return producer_schema.dump(producer_utils.post_producer(args)).data, 201


class ProducerRest(Resource):

    @account_access_required
    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            producer = producer_schema.dump(producer_utils.get_producer_by_id(kwargs['producer_id'])).data
            return caching_utils.cache_json_and_get(path=path, response=producer), 200
        else:
            return cache, 200

    @account_access_required
    def put(self, **kwargs):
        args = parser.parse_args()
        return producer_schema.dump(producer_utils.put_producer(args, kwargs['producer_id'])).data, 201

    @account_access_required
    def delete(self, **kwargs):
        return producer_utils.delete_producer_by_id(kwargs['producer_id']), 201


class ProducerOrders(Resource):

    @account_access_required
    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            orders = order_schema_list.dump(order_utils.get_orders_by_producer_id(kwargs['producer_id'])).data
            return caching_utils.cache_json_and_get(path=path, response=orders), 200
        else:
            return cache, 200


class ProductsByProducer(Resource):

    @account_access_required
    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            products = product_schema_list.dump(product_utils.get_products_by_producer_id(kwargs['producer_id'])).data
            return caching_utils.cache_json_and_get(path=path, response=products), 200
        else:
            return cache, 200


class UploadImageProducer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('image_data', location='form')

    def post(self, producer_id):
        args = self.parser.parse_args()
        return producer_utils.upload_producer_image(producer_id, args['image_data']), 201


class ProducerNamesByCategoryName(Resource):

    @get_cache
    def get(self, path, cache, **kwargs):
        if cache is None:
            names = producer_utils.get_producer_names_by_category_name(kwargs['category_name'])
            return caching_utils.cache_json_and_get(path=path, response=names), 200
        else:
            return cache, 200


class ProducerNameById(Resource):
    def get(self, producer_id):
        return {"producer_name": producer_utils.get_producer_name_by_id(producer_id)}


class ProducerRating(Resource):
    def get(self, **kwargs):
        return {'rating': producer_utils.get_producer_rating_by_id(kwargs['producer_id'])}, 200


def create_new_trello_board_and_commit(board_name, trello_token, current_user):
    create_new_board.apply_async(
        (board_name, trello_token),
        link=commit_change.s(trello_token, current_user.id)
    )


class ProducerLinkTrelloAccount(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('trello_token', location='json', required=True)
    parser.add_argument('board_name', location='json', required=True)

    @account_access_required
    def post(self, **kwargs):
        args = self.parser.parse_args()
        create_new_trello_board_and_commit(
            args['board_name'],
            args['trello_token'],
            current_user
        )
        # board_id = create_new_board(args['board_name'], args['trello_token'])
        # current_user.link_trello_account(args['trello_token'], board_id)
        # db.session.commit()


        return {}, 200

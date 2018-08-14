from flask_restful import Resource, abort, reqparse


from app.marshmallow_schemas import OrderSchema

from app import db

from app.models import Order

order_schema = OrderSchema()


parser = reqparse.RequestParser()
parser.add_argument('total_cost')
parser.add_argument('order_items_json')
parser.add_argument('delivery_method')
parser.add_argument('delivery_address')
parser.add_argument('consumer_phone')
parser.add_argument('consumer_email')
parser.add_argument('consumer_id')
parser.add_argument('producer_id')
parser.add_argument('status')


def abort_if_order_doesnt_exist(order_id):
    if Order.query.get(order_id) is None:
        abort(404, message='Order {} doesn\'t exist'.format(order_id))


def abort_if_consumer_doesnt_exist(consumer_id):
    if Order.query.get(consumer_id) is None:
        abort(404, message='Consumer {} doesn\'t exist'.format(consumer_id))


def abort_if_producer_doesnt_exist(producer_id):
    if Order.query.get(producer_id) is None:
        abort(404, message='Producer {} doesn\'t exist'.format(producer_id))


class GlobalOrders(Resource):

    def get(self):
        return [order_schema.dump(order).data for order in Order.query.all()]

    def post(self):
        args = parser.parse_args()
        new_order = Order(total_cost=args['total_cost'], order_items_json=['order_items_json'],
                          delivery_method=args['delivery_method'], delivery_address=args['delivery_address'],
                          consumer_phone=args['consumer_phone'], consumer_email=args['consumer_email'],
                          consumer_id=args['consumer_id'], producer_id=args['producer_id'])
        db.session.add(new_order)
        db.session.commit()
        return order_schema.dump(new_order).data, 201


class Orders(Resource):
    def get(self, order_id):
        abort_if_order_doesnt_exist(order_id)
        return order_schema.dump(Order.query.get(order_id)).data

    def put(self, order_id):
        abort_if_order_doesnt_exist(order_id)
        args = parser.parse_args()
        order = Order.query.get(order_id)
        if args['status'] is not None:
            order.change_status(args['status'])
        db.session.commit()
        return order_schema.dump(order).data, 201


class ConsumerOrders(Resource):

    def get(self, consumer_id):
        abort_if_consumer_doesnt_exist(consumer_id)
        return [order_schema.dump(order).data for order in Order.query.filter_by(consumer_id=consumer_id).all()]


class ProducerOrders(Resource):
    def get(self, producer_id):
        abort_if_producer_doesnt_exist(producer_id)
        return [order_schema.dump(order).data for order in Order.query.filter_by(producer_id=producer_id).all()]


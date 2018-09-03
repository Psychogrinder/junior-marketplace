from flask_restful import abort
import marketplace.api_folder.api_utils as utils
from marketplace import email_tools
from marketplace.api_folder.schemas import consumer_sign_up_schema
from marketplace.models import Consumer


class ConsumerRepository:

    def __init__(self, session):
        self.session = session

    def abort_or_get(self, consumer_id):
        consumer = Consumer.query.filter_by(entity='consumer').filter_by(id=consumer_id).first()
        if consumer is None:
            abort(404, message='Consumer with id = {} doesn\'t exists'.format(consumer_id))
        return consumer

    def get_by_id(self, consumer_id):
        return self.abort_or_get(consumer_id)

    def get_all(self):
        return Consumer.query.filter_by(entity='consumer').all()

    def post(self, args):
        utils.validate_registration_data(args['email'], args['password'])
        utils.check_email_uniqueness(args['email'])
        new_consumer = consumer_sign_up_schema.load(args).data
        self.session.add(new_consumer)
        self.session.commit()
        email_tools.send_confirmation_email(new_consumer.email)
        return new_consumer

    def put(self, args, consumer_id):
        consumer = self.get_by_id(consumer_id)
        args['id'] = None
        for k, v in args.items():
            if v:
                setattr(consumer, k, v)
        self.session.commit()
        return consumer

    def delete_by_id(self, consumer_id):
        consumer = self.get_by_id(consumer_id)
        self.session.delete(consumer)
        self.session.commit()
        return {"message": "Consumer with id {} has been deleted".format(consumer_id)}

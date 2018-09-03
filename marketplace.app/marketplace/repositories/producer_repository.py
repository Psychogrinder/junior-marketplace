from flask_restful import abort

from marketplace.api_folder.api_utils import abort_if_producer_doesnt_exist_or_get
from marketplace.api_folder.schemas import producer_sign_up_schema
from marketplace.models import Producer
import marketplace.api_folder.api_utils as utils


class ProducerRepository:
    def __init__(self, session):
        self.session = session

    def abort_or_get(self, producer_id):
        producer = Producer.query.filter_by(entity='producer').filter_by(id=producer_id).first()
        if producer is None:
            abort(404, message='Producer with id = {} doesn\'t exists'.format(producer_id))
        return producer

    def get_by_id(self, producer_id):
        return abort_if_producer_doesnt_exist_or_get(producer_id)

    def get_by_name(self, name):
        return Producer.query.filter_by(name=name).first()

    def get_all(self):
        return Producer.query.filter_by(entity='producer').all()

    def post(self, args):
        utils.validate_registration_data(args['email'], args['password'])
        utils.check_email_uniqueness(args['email'])
        utils.check_producer_name_uniqueness(args['name'])
        new_producer = producer_sign_up_schema.load(args).data
        self.session.add(new_producer)
        self.session.commit()
        utils.email_tools.send_confirmation_email(new_producer.email)
        return new_producer

    def put(self, args, producer_id):
        producer = self.get_by_id(producer_id)
        args['id'] = None
        for k, v in args.items():
            if v:
                setattr(producer, k, v)
        self.session.commit()
        return producer

    def delete(self, producer_id):
        producer = self.get_by_id(producer_id)
        self.session.delete(producer)
        self.session.commit()
        return {"message": "Producer with id {} has been deleted successfully".format(producer_id)}

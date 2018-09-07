from marketplace import email_tools, db
from marketplace.api_folder.schemas import consumer_sign_up_schema
from marketplace.api_folder.utils.abortions import abort_if_consumer_doesnt_exist_or_get
from marketplace.api_folder.utils.checkers import check_email_uniqueness
from marketplace.api_folder.utils.uploaders import upload_image
from marketplace.api_folder.utils.validators import validate_registration_data
from marketplace.models import Consumer


def get_consumer_by_id(consumer_id):
    return abort_if_consumer_doesnt_exist_or_get(consumer_id)


def get_all_consumers():
    return Consumer.query.filter_by(entity='consumer').all()


def post_consumer(args):
    validate_registration_data(args['email'], args['password'])
    check_email_uniqueness(args['email'])
    new_consumer = consumer_sign_up_schema.load(args).data
    db.session.add(new_consumer)
    db.session.commit()
    # временно закоменчено, потому-что иначе ломает
    # email_tools.send_confirmation_email(new_consumer.email)
    return new_consumer


def put_consumer(args, consumer_id):
    consumer = get_consumer_by_id(consumer_id)
    args['id'] = None
    for k, v in args.items():
        if v:
            setattr(consumer, k, v)
    db.session.commit()
    return consumer


def delete_consumer_by_id(consumer_id):
    consumer = get_consumer_by_id(consumer_id)
    db.session.delete(consumer)
    db.session.commit()
    return {"message": "Consumer with id {} has been deleted".format(consumer_id)}


def upload_consumer_image(consumer_id, files):
    consumer = get_consumer_by_id(consumer_id)
    return upload_image(consumer, files)

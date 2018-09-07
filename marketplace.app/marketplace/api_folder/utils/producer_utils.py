import os
import shutil

from marketplace import db, email_tools
from marketplace.api_folder.schemas import producer_sign_up_schema
from marketplace.api_folder.utils.abortions import abort_if_producer_doesnt_exist_or_get
from marketplace.api_folder.utils.checkers import check_email_uniqueness, check_producer_name_uniqueness
from marketplace.api_folder.utils.uploaders import upload_image
from marketplace.api_folder.utils.validators import validate_registration_data
from marketplace.models import Producer, Category, Product


def get_producer_by_id(producer_id):
    return abort_if_producer_doesnt_exist_or_get(producer_id)


def get_producer_by_name(name):
    return Producer.query.filter_by(name=name).first()


def get_producer_name_by_id(producer_id):
    return db.session.query(Producer.name).filter(Producer.id == producer_id).first()[0]


def get_all_producers():
    return Producer.query.filter_by(entity='producer').all()


def post_producer(args):
    validate_registration_data(args['email'], args['password'])
    check_email_uniqueness(args['email'])
    check_producer_name_uniqueness(args['name'])
    new_producer = producer_sign_up_schema.load(args).data
    db.session.add(new_producer)
    db.session.commit()
    # make directory to store this producer's images
    os.mkdir(os.path.join(os.getcwd(), 'marketplace/static/img/user_images/' + str(new_producer.id) + '/'))
    # временно закоменчено, потому-что иначе ломает
    # email_tools.send_confirmation_email(new_producer.email)
    return new_producer


def put_producer(args, producer_id):
    producer = get_producer_by_id(producer_id)
    args['id'] = None
    for k, v in args.items():
        if v:
            setattr(producer, k, v)
    db.session.commit()
    return producer


def delete_producer_by_id(producer_id):
    producer = get_producer_by_id(producer_id)
    # TODO перенести функцию get_products_by_producer_id из product_utils в producer_utils
    # producer_products = get_products_by_producer_id(producer_id)
    producer_products = Product.query.filter_by(producer_id=producer_id).all()
    for product in producer_products:
        db.session.delete(product)
    image_directory_path = os.path.join(os.getcwd(), 'marketplace/static/img/user_images/' + str(producer_id) + '/')
    shutil.rmtree(image_directory_path)
    db.session.delete(producer)
    db.session.commit()
    return {"message": "Producer with id {} has been deleted successfully".format(producer_id)}


def upload_producer_image(producer_id, files):
    producer = get_producer_by_id(producer_id)
    return upload_image(producer, files, producer_id)


def get_producer_names_by_category_name(category_name):
    category = Category.query.filter_by(name=category_name).first()
    producers = get_all_producers()
    return [producer.name for producer in producers if category in producer.categories]

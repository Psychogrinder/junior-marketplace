from flask import Flask
from flask_assets import Environment, Bundle
from marketplace.config import Development, Production
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
import os
import logging
import redis
import cssmin
import jsmin
from flask_mail import Mail
from influxdb import InfluxDBClient
from raven.contrib.flask import Sentry


app = Flask(__name__)
assets = Environment(app)
app.config.from_object(
    Development if os.getenv('FLASK_ENV') == 'development' else Production
)

if app.config.get('SENTRY_DSN'):
    if os.getenv('CELERY_APP'):
        from raven import Client
        from raven.contrib.celery import register_signal, register_logger_signal
        sentry = Client(app.config['SENTRY_DSN'])
        register_logger_signal(sentry)
        register_signal(sentry)
    else:
        sentry = Sentry(app, dsn=app.config['SENTRY_DSN'], logging=True, level=logging.ERROR)
from marketplace import _celery

mail = Mail(app)
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
ma = Marshmallow(app)
api = Api(app, prefix='/api/v1')
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
celery = _celery.make_celery(app)
cache = redis.Redis(host=app.config['CACHE_STORAGE_HOST'], port=app.config['CACHE_STORAGE_PORT'],
                    db=app.config['CACHE_STORAGE_DB'])
REDIS_STORAGE_TIME = app.config['REDIS_STORAGE_TIME']
COMMENTS_PER_PAGE = app.config['COMMENTS_PER_PAGE']
PRODUCTS_PER_PAGE = app.config['PRODUCTS_PER_PAGE']
ORDERS_PER_PAGE = app.config['ORDERS_PER_PAGE']

influx_client = InfluxDBClient(
    host=app.config['INFLUXDB_HOST'],
    database=app.config['INFLUXDB_DATABASE'],
    username=app.config['INFLUXDB_USER'],
    password=app.config['INFLUXDB_PASSWORD'],
)


from marketplace import models, views, api_routes
from marketplace.models import Admin

css = Bundle('style/variable.scss', 'style/base.scss', 'style/header.css', 'style/footer.css', 'style/catalog.css',
             'style/modal.css', 'style/category.scss', 'style/breadcrumbs.css', 'style/card.css', 'style/cart.scss',
             'style/edit_profile.css', 'style/profile.css', 'style/order_history.css', 'style/edit_product.css',
             'style/producer_products.scss', 'style/producer_orders.css', 'style/order_registration.css',
             'style/sing.css', 'style/validation.css', 'style/404.scss', 'style/croppie.css', 'style/image_crop.css',
             'style/input_file.css', 'style/reset_password.css',
             filters=['pyscss', 'cssmin'], output='bundle.min.css')

assets.register('css_all', css)

js = Bundle('script/quantity.js', 'script/table_view.js', 'script/edit_product.js', 'script/registration_consumer.js',
            'script/authorisation.js', 'script/registration_producer.js', 'script/menu_backlighting.js',
            'script/edit_consumer_profile.js', 'script/edit_producer_profile.js',
            'script/cart.js', 'script/create_product.js', 'script/order_placement.js', 'script/order_history.js',
            'script/i18n/ru.js', 'script/edit_product_post.js', 'script/producer_orders.js', 'script/phone_mask.js',
            'script/category.js', 'script/orders_badge.js', 'script/hullabaloo.js', 'script/producer_products.js',
            'script/delete_product.js', 'script/delete_producer.js', 'script/delete_consumer.js', 'script/croppie.js',
            'script/image_crop.js', 'script/get_comments.js', 'script/review.js', 'script/jquery.inputmask.bundle.js',
            'script/password_recovery.js',

            filters=['jsmin'], output='app.min.js')

assets.register('js_all', js)

if __name__ == '__main__':
    app.run(port=8000)

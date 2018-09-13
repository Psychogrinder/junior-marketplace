from flask import Flask
from flask_assets import Environment, Bundle
from marketplace.config import Development, Production
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
import os
import redis
import cssmin
import jsmin
from flask_mail import Mail
from marketplace import _celery

app = Flask(__name__)
assets = Environment(app)
app.config.from_object(
    Development if os.getenv('FLASK_ENV') == 'development' else Production
)
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

from marketplace import models, views, api_routes
from marketplace.models import Admin

css = Bundle('style/base.css', 'style/header.css', 'style/footer.css', 'style/catalog.css', 'style/modal.css',
             'style/category.css',
             'style/breadcrumbs.css', 'style/card.css', 'style/cart.css', 'style/edit_profile.css', 'style/profile.css',
             'style/order_history.css', 'style/producer_products.css', 'style/edit_product.css',
             'style/producer_products.css', 'style/producer_orders.css', 'style/order_registration.css',
             'style/sing.css', 'style/validation.css', 'style/404.css', 'style/croppie.css', 'style/image_crop.css',
             'style/input_file.css', 'style/reset_password.css',
             filters=['pyscss','cssmin'], output='bundle.min.css')

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

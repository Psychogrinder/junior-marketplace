from flask import Flask
from flask_assets import Environment, Bundle
from marketplace.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
import os
import cssmin
import jsmin
from flask_mail import Mail
from marketplace import _celery

app = Flask(__name__)
assets = Environment(app)
app.config.from_object(Config)
mail = Mail(app)
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
ma = Marshmallow(app)
api = Api(app, prefix='/api/v1')
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)
db.init_app(app)
celery = _celery.make_celery(app)

from marketplace import models, views, api_routes

css = Bundle('style/base.css', 'style/header.css', 'style/footer.css', 'style/catalog.css', 'style/modal.css',
             'style/category.css',
             'style/breadcrumbs.css', 'style/card.css', 'style/cart.css', 'style/edit_profile.css', 'style/profile.css',
             'style/order_history.css', 'style/producer_products.css', 'style/edit_product.css',
             'style/producer_products.css', 'style/producer_orders.css', 'style/order_registration.css',
             'style/sing.css',
             filters=['cssmin'], output='bundle.min.css')

assets.register('css_all', css)

js = Bundle('script/quantity.js', 'script/table_view.js', 'script/edit_product.js', 'script/registration_consumer.js',
            'script/authorisation.js', 'script/registration_producer.js', 'script/menu_backlighting.js',
            'script/edit_consumer_profile.js', 'script/edit_producer_profile.js',
            'script/cart.js', 'script/edit_product_post.js', 'script/create_product.js',
            filters=['jsmin'], output='app.min.js')

assets.register('js_all', js)

if __name__ == '__main__':
    app.run(port=8000)

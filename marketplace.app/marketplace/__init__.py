from flask import Flask, render_template
from flask_assets import Environment, Bundle
from marketplace.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
import cssmin


app = Flask(__name__)
assets = Environment(app)
app.config.from_object(Config)
ma = Marshmallow(app)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)

from marketplace import models, views

css = Bundle('style/authorization.css','style/header.css', 'style/footer.css', 'style/catalog.css',
             filters=['cssmin'], output='bundle.min.css')
assets.register('css_all', css)


if __name__=='__main__':
    app.run(port=8000)

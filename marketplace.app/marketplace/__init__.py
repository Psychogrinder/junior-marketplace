from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(Config)
ma = Marshmallow(app)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)

from marketplace import models, views

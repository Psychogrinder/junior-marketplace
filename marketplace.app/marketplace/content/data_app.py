import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(os.path.realpath(dir_path))
print(dir_path)
sys.path.insert(0, dir_path)
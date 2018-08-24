import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost/marketplace.db'
    UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/user_images'

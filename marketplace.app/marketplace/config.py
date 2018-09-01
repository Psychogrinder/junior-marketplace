from dotenv import load_dotenv
import os

load_dotenv()


class Config(object):

    SQLALCHEMY_DATABASE_URI = (
        os.getenv('SQLALCHEMY_DATABASE_URI')
        or 'postgresql://postgres:1234@localhost/marketplace.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/user_images'
    SECRET_KEY = 'secret-key'
    SECURITY_PASSWORD_SALT = 'secret-salt'

    MAIL_SERVER = 'smtp.rambler.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_USERNAME = 'xtramarket'
    MAIL_PASSWORD = 'dfkkJK931NNN12'
    # MAIL_DEFAULT_SENDER = 'xtramarket@rambler.ru'


    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL') or 'redis://localhost:6379/0',

    CACHE_STORAGE_HOST = 'localhost'
    CACHE_STORAGE_PORT = 6379
    CACHE_STORAGE_DB = 1
    REDIS_STORAGE_TIME = 1

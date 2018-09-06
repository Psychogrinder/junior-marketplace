from dotenv import load_dotenv
import os

load_dotenv()


class Base(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.path.dirname(
        os.path.abspath(__file__)),
        'static', 'img', 'user_images'
    )

    USER_IMAGE_PRODUCTS_SIZE = 255, 150
    USER_IMAGE_PRODUCER_LOGO_SIZE = 250, 300
    ALLOWED_UPLOAD_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp'])
    USER_IMAGE_DEFAULT_FORMAT = 'webp'

    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_DEFAULT_SENDER = 'xtramarket@rambler.ru'


    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL') or 'redis://localhost:6379/9'

    CACHE_STORAGE_HOST = 'localhost'
    CACHE_STORAGE_PORT = 6379
    CACHE_STORAGE_DB = 1
    REDIS_STORAGE_TIME = 1


class Development(Base):
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('SQLALCHEMY_DATABASE_URI')
        or 'postgresql://postgres:1234@localhost/marketplace.db'
    )

    SECRET_KEY = 'secret-key'
    SECURITY_PASSWORD_SALT = 'secret-salt'

    CACHE_STORAGE_HOST = os.getenv('CACHE_STORAGE_HOST') or 'localhost'


class Production(Base):
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL')

    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    CACHE_STORAGE_HOST = 'redis'
    CACHE_STORAGE_PORT = 6379
    CACHE_STORAGE_DB = 1
    REDIS_STORAGE_TIME = 1

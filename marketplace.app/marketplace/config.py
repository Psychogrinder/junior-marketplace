from dotenv import load_dotenv
import os


load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost/marketplace.db'
    SECRET_KEY = 'secret-key'
    SECURITY_PASSWORD_SALT = 'secret-salt'

    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    CELERY_BROKER_URL='redis://localhost:6379/0',

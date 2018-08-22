from dotenv import load_dotenv
load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost/marketplace.db'
    SECRET_KEY = 'secret-key'
    SECURITY_PASSWORD_SALT = 'secret-salt'


    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True

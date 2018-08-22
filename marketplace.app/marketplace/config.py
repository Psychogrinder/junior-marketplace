class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost/marketplace.db'
    SECRET_KEY = 'secret-key'
    SECURITY_PASSWORD_SALT = 'secret-salt'

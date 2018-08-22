from itsdangerous import URLSafeSerializer, BadSignature
from marketplace import app


def generate_confirmation_token(user_email):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(user_email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT']
        )
    except BadSignature:
        return None
    return email

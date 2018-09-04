from marketplace.models import User


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

from flask_login import login_user, logout_user

from marketplace.api_folder.utils.user_utils import get_user_by_email


def login(args):
    user = get_user_by_email(args['email'])
    if user is None or not user.check_password(args['password']):
        return False
    # Вместо True потом добавить возможность пользователю выбирать запоминать его или нет
    login_user(user, True)
    return {"id": user.id, "entity": user.entity}


def logout():
    logout_user()
    return 'Logout'

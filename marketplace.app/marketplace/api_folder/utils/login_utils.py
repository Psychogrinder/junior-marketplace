from flask_login import login_user, logout_user, current_user

from marketplace.api_folder.utils.abortions import invalid_email_or_password, \
    admin_rights_required, account_access_denied
from marketplace.api_folder.utils.user_utils import get_user_by_email


def login(args):
    user = get_user_by_email(args['email'])
    if user is None or not user.check_password(args['password']):
        invalid_email_or_password()
    # Вместо True потом добавить возможность пользователю выбирать запоминать его или нет
    login_user(user, True)
    return {"id": user.id, "entity": user.entity}


def logout():
    logout_user()
    return 'Logout'


def key_ends_with_id(items):
    for key in items.keys():
        if key.endswith('id'):
            return key

    return None


def login_as_admin_required(rest_function):
    def admin_required_wrapper(self, *args, **kwargs):
        if current_user.is_authenticated and current_user.entity == 'admin':
            return rest_function(self, *args, **kwargs)
        else:
            admin_rights_required()

    return admin_required_wrapper


def account_access_required(rest_function):
    def account_access_wrapper(self, *args, **kwargs):
        id = kwargs[key_ends_with_id(kwargs)]
        if current_user.is_authenticated and current_user.id == id:
            return rest_function(self, *args, **kwargs)
        else:
            account_access_denied()

    return account_access_wrapper

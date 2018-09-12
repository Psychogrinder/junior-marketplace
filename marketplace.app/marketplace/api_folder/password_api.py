from flask_restful import Resource, reqparse
from .utils import user_utils
from marketplace import email_tools


class PasswordRecovery(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, location='form')

    def post(self):
        email = self.parser.parse_args()['email']
        if user_utils.get_user_by_email(email) is None:
            return False, 400
        email_tools.send_password_recovery_email(email)
        return True, 200

from flask_restful import Resource, reqparse
from .utils import user_utils
from marketplace import email_tools


class PasswordRecovery(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, location='form')

    def post(self):
        email = self.parser.parse_args()['email']
        user = user_utils.get_user_by_email(email)
        if user is None:
            return False, 400
        contact = user.first_name if user.entity == 'consumer' else user.person_to_contact
        email_tools.send_password_recovery_email(email, contact)
        return True, 200

from flask_restful import Resource, reqparse
from marketplace.models import Producer, User, Consumer
from marketplace import email_tools


class PasswordRecovery(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, location='form')

    def post(self):
        email = self.parser.parse_args()['email']
        try:
            if User.query.filter_by(email=email).first().entity == 'producer':
                contact = Producer.query.filter_by(email=email).first().person_to_contact
            else:
                contact = Consumer.query.filter_by(email=email).first().first_name
        except AttributeError:
            return False, 400
        email_tools.send_password_recovery_email(email, contact)
        return True, 200

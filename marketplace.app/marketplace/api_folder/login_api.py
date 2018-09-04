from flask_restful import Resource, reqparse
from marketplace.api_folder.utils import login_utils

login_args = ['email', 'password']
parser = reqparse.RequestParser()

for arg in login_args:
    parser.add_argument(arg)


class Login(Resource):
    def post(self):
        args = parser.parse_args()
        return login_utils.login(args), 201

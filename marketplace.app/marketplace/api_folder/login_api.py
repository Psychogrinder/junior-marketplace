from flask_restful import Resource, reqparse
import marketplace.api_folder.api_utils as utils

login_args = ['email', 'password']
parser = reqparse.RequestParser()

for arg in login_args:
    parser.add_argument(arg)


class Login(Resource):
    def post(self):
        args = parser.parse_args()
        return utils.login(args), 201

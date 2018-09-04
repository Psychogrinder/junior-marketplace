from flask_restful import Resource
from marketplace.api_folder.utils import login_utils


class Logout(Resource):
    def get(self):
        return login_utils.logout(), 201

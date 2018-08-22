from flask_restful import Resource
import marketplace.api_folder.api_utils as utils


class Logout(Resource):
    def get(self):
        return utils.logout(), 201

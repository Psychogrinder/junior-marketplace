from flask_restful import Resource
import marketplace.api_folder.api_utils as utils
from flask import request


class UploadImage(Resource):
    def post(self, user_id):
        return utils.upload_image(user_id, request.files), 201

from flask_restful import Resource
from flask import request


class TrelloWebHook(Resource):

    def post(self):
        print(request.json())
        return {}, 200
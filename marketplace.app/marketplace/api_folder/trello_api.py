from flask_restful import Resource
from flask import request
from marketplace.error_reports import send_report
from marketplace.trello_integrations import change_order_status


class TrelloWebHook(Resource):

    def post(self):
        change_order_status(request.json)
        return {}, 200

    def head(self):
        return {}, 200

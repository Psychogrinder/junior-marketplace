from flask_restful import Resource, reqparse
import marketplace.api_folder.utils.chat_utils as chat_utils


class ChatHistory(Resource):
    def get(self, room: int):
        return chat_utils.get_messages_by_room(room), 200


message_parser = reqparse.RequestParser()
message_parser.add_argument('page')
message_parser.add_argument('consumer_id')


class MessageStatus(Resource):
    def post(self):
        args = message_parser.parse_args()
        return chat_utils.set_message_status(args['order_id'], int(args['entity']))

from flask_restful import Resource
import marketplace.api_folder.utils.chat_utils as chat_utils


class ChatHistory(Resource):
    def get(self, room: int):
        return chat_utils.get_messages_by_room(room), 200

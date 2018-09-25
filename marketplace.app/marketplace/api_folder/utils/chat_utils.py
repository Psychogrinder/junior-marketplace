# messages - то коллекция всех сообщений в базе данных message-history
from marketplace.chat import messages


def get_messages_by_room(room: int):
    result = []
    for message in messages.find({"room": room}):
        del message['_id']
        result.append(message)
    return result

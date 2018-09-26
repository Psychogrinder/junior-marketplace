# messages - то коллекция всех сообщений в базе данных message-history
from marketplace.chat import messages
from marketplace.models import Order


def get_messages_by_room(room: int) -> list:
    result = []
    for message in messages.find({"room": room}):
        del message['_id']
        result.append(message)
    return result


def set_message_status(order_id: int, entity: str):
    """
    Меняет у Order значение полей "имеются непрочитанные сообщения" на False.
    :param order_id: соответствует номеру комнаты
    :param entity: либо producer, либо consumer.
    """
    order = Order.query.get(order_id)
    if entity == 'producer':
        order.has_unread_producer_messages = False
    # ... или покупателя
    elif entity == 'consumer':
        order.has_unread_consumer_messages = False
    db.session.commit()
    return True

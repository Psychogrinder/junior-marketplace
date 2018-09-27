from marketplace import socketio, mongo_client, db
from marketplace.models import Order
from flask_socketio import emit, join_room
from flask_login import current_user
from datetime import datetime

chat_db = mongo_client['message-history']
messages = chat_db['messages']


def get_messages_by_room(room: int) -> list:
    result = []
    for message in messages.find({"room": room}):
        # _id не нужен и не JSON serializable
        del message['_id']
        result.append(message)
    return result


def set_message_status(order_id: int, entity: str):
    """
    Меняет у Order значение полей "имеются непрочитанные сообщения" на 0.
    :param order_id: соответствует номеру комнаты
    :param entity: либо producer, либо consumer.
    """
    order = Order.query.get(order_id)
    if entity == 'producer':
        order.unread_producer_messages = 0
    # ... или покупателя
    elif entity == 'consumer':
        order.unread_consumer_messages = 0
    db.session.commit()
    return True


@socketio.on('connected', namespace='/chat')
def on_connection(data):
    print('A new connection: ' + str(data))


@socketio.on('join', namespace='/chat')
def on_join(data):
    join_room(data['room'])


def handle_message(message, entity, order_id):
    # Сохраняем сообщение в базу данных message-history
    messages.insert_one(message)
    # Указываем в заказе, что есть непрочитанные сообщения от производителя...
    order = Order.query.get(order_id)
    if entity == 'producer':
        order.unread_producer_messages += 1
    # ... или покупателя
    elif entity == 'consumer':
        order.unread_consumer_messages += 1
    db.session.commit()


@socketio.on('send_to_room', namespace='/chat')
def send_room_message(data):
    # Добавляем в сообщение нужные параметры: имя, ссылку на фото, время
    if current_user.entity == 'producer':
        username = current_user.person_to_contact
    elif current_user.entity == 'consumer':
        username = f'{current_user.first_name} {current_user.last_name}'
    message = {
        'room': data['room'],
        'username': username,
        'photo_url': current_user.photo_url,
        'timestamp': datetime.now().strftime('%H:%M %d.%m.%Y'),
        'body': data['body'],
    }
    # отсылаем сообщение в указанную комнату
    emit('response',
         message,
         room=data['room']
         )
    handle_message(message, data['entity'], data['room'])

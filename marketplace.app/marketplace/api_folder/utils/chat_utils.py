from flask_socketio import emit, join_room
from flask_login import current_user
from datetime import datetime
from sqlalchemy.sql import func

from marketplace import socketio, mongo_client, db
from marketplace.models import Order, User

chat_db = mongo_client['message-history']
messages = chat_db['messages']


def get_number_of_unread_messages_by_user_id(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    if user.entity == 'consumer':
        orders = Order.query.filter_by(consumer_id=user.id).all()
        number_of_messages = sum(order.unread_producer_messages for order in orders)
    elif user.entity == 'producer':
        orders = Order.query.filter_by(producer_id=user.id).all()
        number_of_messages = sum(order.unread_consumer_messages for order in orders)
    return number_of_messages


def get_messages_by_room(room: int) -> list:
    result = []
    for message in messages.find({"room": room}):
        # _id не нужен и не JSON serializable
        del message['_id']
        result.append(message)
    return result


def set_message_status(order_id: int, entity: str):
    """
    Меняет у Order значение полей "непрочитанные сообщения" на 0.
    :param order_id: соответствует номеру комнаты
    :param entity: либо producer, либо consumer.
    """
    order = Order.query.get(order_id)
    if entity == 'producer':
        order.unread_producer_messages = 0
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
    if current_user.is_authenticated:
        emit('response',
             message,
             room=data['room']
             )
        handle_message(message, data['entity'], data['room'])
    else:
        return False

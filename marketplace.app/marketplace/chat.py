from marketplace import socketio, mongo_client, db
from marketplace.models import Order
from flask_socketio import emit, join_room, rooms
from flask_login import current_user
from datetime import datetime

chat_db = mongo_client['message-history']
messages = chat_db['messages']


@socketio.on('connected', namespace='/chat')
def on_connection(data):
    print('_____GOT A NEW CONNECTION_START____')
    print('received my event: ' + str(data))
    print('_____GOT A NEW CONNECTION_END____')


@socketio.on('join', namespace='/chat')
def on_join(data):
    room = data['room']
    print('_____GOT A NEW JOIN_START____')
    print(f'User {current_user.id} joined room {room}')
    print(f'This is the message history start')
    import pprint
    for message in messages.find({"room": data['room']}):
        pprint.pprint(message)
    print(f'This is the message history end')
    print('_____GOT A NEW JOIN_END____')
    join_room(data['room'])


def handle_message(message, entity, order_id):
    # Сохраняем сообщение в базу данных message-history
    message_id = messages.insert_one(message).inserted_id
    print(f'its id {message_id}')
    # Указываем в заказе, что есть непрочитанные сообщения от производителя...
    order = Order.query.get(order_id)
    if entity == 'producer':
        order.has_unread_producer_messages = True
    # ... или покупателя
    elif entity == 'consumer':
        order.has_unread_consumer_messages = True
    db.session.commit()


@socketio.on('send_to_room', namespace='/chat')
def send_room_message(data):
    """
    Отсылает сообщение в определённую комнату.
    :param data:
    :return:
    """
    print('_____GOT A NEW message_START____')
    print(f'New message -  {data["body"]} in room {data["room"]}')
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
        'read': False
    }
    emit('response',
         message,
         room=data['room']
         )
    print('_____GOT A NEW message_END____')
    handle_message(message, data['entity'], data['room'])

from marketplace import socketio
from flask_socketio import emit, join_room, rooms
from flask_login import current_user
from datetime import datetime


def message_received():
    print('message was received!!!')


@socketio.on('connected', namespace='/chat')
def on_connection(data):
    print('_____GOT A NEW CONNECTION_START____')
    print('received my event: ' + str(data))
    print('_____GOT A NEW CONNECTION_END____')

    emit('my response', data, callback=message_received)


@socketio.on('join', namespace='/chat')
def on_join(data):
    room = data['room']
    print('_____GOT A NEW JOIN_START____')
    print(f'User {current_user.id} joined room {room}')
    print('_____GOT A NEW JOIN_END____')
    join_room(data['room'])


@socketio.on('send_to_room', namespace='/chat')
def send_room_message(data):
    room = data['room']
    message = data['message']
    print('_____GOT A NEW message_START____')
    print('this user rooms are', rooms())
    print(f'New message -  {message} in room {room}')
    print('_____GOT A NEW message_END____')

    emit('response',
         {'message': data['message'],
          'room': data['room'],
          'username': 'TEMP_NAME',
          'timestamp': datetime.now().strftime('%d.%m.%y')},
         room=data['room'])

from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_cors import CORS
from .config import Configuration
from .routes import session, channel
from .models import *
import jwt


app = Flask(__name__)
app.config.from_object(Configuration)
socket = SocketIO(app, cors_allowed_origins="*")
CORS(app)
app.register_blueprint(session.bp)
app.register_blueprint(channel.bp)
db.init_app(app)
Migrate(app, db)


@app.route('/')
def hello_world():
    return 'Hi!! ::)'


@socket.on('connect')
def test_connect():
    print('Client connected')


@socket.on('disconnect')
def disconnect():
    print('Client disconnected')


@socket.on('join')
def join(data):
    # print('Client joined')
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    container = Container.query.filter_by(id=data['channelId']).first()
    room = container.id
    join_room(room)
    # print(f'{current_user.username} entered room {container.id}')
    emit('message',
         {'msg': {'message': f' --- {current_user.username}'
                  f' has entered {container.title}! ---'
                  }
          },
         broadcast=True,
         room=room
         )


@socket.on('leave')
def leave(data):
    # print('Client left')
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    container = Container.query.filter_by(id=data['channelId']).first()
    room = int(data['channelId'])
    leave_room(room)
    # print(f'{current_user.username} left room {container.id}')
    if container:
        emit('message',
             {'msg': {'message': f' --- {current_user.username}'
                      f' has left {container.title}! ---'
                      }
              },
             broadcast=True,
             room=room
             )


@socket.on('join_channel')
def join_channel(data):
    # print('adding new member to channel')
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    channel = Container.query.filter_by(id=data['channelId']).first()
    channel.members.append(current_user)
    db.session.commit()
    room = channel.id
    channels = Container.query.filter_by(is_channel=True).all()
    returnchannels = dict((c.id, {
        'title': c.title,
        'topic': c.topic,
        'adminId': c.admin_id,
        'users': c.user_list,
    }) for c in channels)
    emit('new_member',
         {'channels': returnchannels,
          'containers': current_user.container_list,
          'new_member_id': current_user.id,
          },
         broadcast=True,
         room=room
         )


@socket.on('leave_channel')
def leave_channel(data):
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    channel = Container.query.filter_by(id=data['channelId']).first()
    channel.members.remove(current_user)
    db.session.commit()
    room = channel.id
    channels = Container.query.filter_by(is_channel=True).all()
    returnchannels = dict((c.id, {
        'title': c.title,
        'topic': c.topic,
        'adminId': c.admin_id,
        'users': c.user_list,
    }) for c in channels)
    emit('member_left',
         {'channels': returnchannels,
          'containers': current_user.container_list,
          'old_member_id': current_user.id,
          },
         broadcast=True,
         room=room
         )


@socket.on('get_history')
def get_history(data):
    # print('getting history')
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    messages = Message.query.filter_by(container_id=data['channelId']).all()
    msgs = {msg.id: {'message': msg.message,
                     'username': msg.messager.username,
                     'avi_url': msg.messager.avi_url,
                     'bio': msg.messager.bio
                     } for msg in messages}
    room = int(data['channelId'])
    emit('history',
         {'history': msgs,
          'userId': current_user.id,
          },
         broadcast=True,
         room=room
         )


@socket.on('message')
def message_sender(data):
    # print('u tried to send message')
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    sender = User.query.filter_by(id=tokenObj['user_id']).first()
    message = data['message']
    new_msg = Message(
        messager=sender,
        container_id=data['channelId'],
        message=message,
    )
    db.session.add(new_msg)
    db.session.commit()
    room = int(data['channelId'])
    send({'msg': {'message': message,
                  'messageId': new_msg.id,
                  'userId': sender.id,
                  'username': sender.username,
                  'avi_url': sender.avi_url,
                  'bio': sender.bio,
                  }
          },
         broadcast=True,
         room=room
         )


@socket.on('typingOn')
def began_typing(data):
    print('began typing')
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    sender = User.query.filter_by(id=tokenObj['user_id']).first()
    room = int(data['channelId'])
    emit('typing',
         {'typingUser': {'userId': sender.id,
                         'isTyping': True,
                         }},
         broadcast=True,
         room=room
         )


@socket.on('typingOff')
def began_typing(data):
    print('stopped typing')
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    sender = User.query.filter_by(id=tokenObj['user_id']).first()
    room = int(data['channelId'])
    emit('typing',
         {'typingUser': {'userId': sender.id,
                         'isTyping': False,
                         }},
         broadcast=True,
         room=room
         )


@socket.on('change_topic')
def change_topic(data):
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    channel = Container.query.filter_by(id=data['channelId']).first()
    if channel.admin == current_user:
        channel.topic = data['newTopic']
        db.session.commit()
    channels = Container.query.filter_by(is_channel=True).all()
    returnchannels = dict((c.id, {
        'title': c.title,
        'topic': c.topic,
        'adminId': c.admin_id,
        'users': c.user_list,
    }) for c in channels)
    room = int(data['channelId'])
    emit('new_topic',
         {'channels': returnchannels,
          'update_msg':  f' --- channel admin {current_user.username}'
          f' has changed the topic to "{channel.topic}" ---'
          },
         broadcast=True,
         room=room
         )


@socket.on('delete_channel')
def delete_channel(data):
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    channel = Container.query.filter_by(id=data['channelId']).first()
    if channel.admin == current_user:
        db.session.delete(channel)
        db.session.commit()
        room = int(data['channelId'])
        emit('channel_deleted',
             broadcast=True,
             room=room
             )

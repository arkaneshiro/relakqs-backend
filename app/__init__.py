from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_cors import CORS
from .config import Configuration
from .routes import session, channel
from .models import db, User, Container, Message
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


@socket.on('join')
def join(data):
    print('Client joined')
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    container = Container.query.filter_by(id=data['channelId']).first()
    room = container.id
    join_room(room)
    print(f'{current_user.username} entered room {container.id}')
    emit('message',
         {'msg': {'message': f'--- {current_user.username}'
                  f' has entered {container.title}! ---'
                  }
          },
         broadcast=True,
         room=room
         )


@socket.on('get_history')
def get_history(data):
    print('getting history')
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    messages = Message.query.filter_by(container_id=data['channelId']).all()
    msgs = {msg.id: {'message': msg.message,
                     'username': msg.messager.username,
                     'avi_url': msg.messager.avi_url,
                     'bio': msg.messager.bio
                     } for msg in messages}
    emit('history',
         {'history': msgs,
          'userId': current_user.id,
          },
         broadcast=True,
         room=int(data['channelId'])
         )


@socket.on('message')
def message_sender(data):
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
    send({'msg': {'message': message,
                  'messageId': new_msg.id,
                  'userId': sender.id,
                  'username': sender.username,
                  'avi_url': sender.avi_url,
                  'bio': sender.bio,
                  }
          },
         broadcast=True,
         room=int(data['channelId'])
         )


@socket.on('leave')
def leave(data):
    print('Client left')
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    container = Container.query.filter_by(id=data['channelId']).first()
    room = container.id
    print(f'{current_user.username} left room {container.id}')
    emit('message',
         {'msg': {'message': f'--- {current_user.username}'
                  f' has left {container.title}! ---'
                  }
          },
         broadcast=True,
         room=room
         )


@socket.on('disconnect')
def disconnect():
    print('Client disconnected')

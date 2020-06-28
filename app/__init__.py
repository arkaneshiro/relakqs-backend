from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_cors import CORS
from .config import Configuration
from .routes import session, channel
from .models import db, User, Container
import jwt


app = Flask(__name__)
app.config.from_object(Configuration)
socket = SocketIO(app, cors_allowed_origins="*")
CORS(app)
app.register_blueprint(session.bp)
app.register_blueprint(channel.bp)
db.init_app(app)
Migrate(app, db)


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
    emit('message',
         {'msg': f'{current_user.username} has entered the chat!'},
         broadcast=True,
         room=room
         )


@socket.on('send_message')
def message_sender(data):
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    message = data['message']
    emit('message',
         {'msg': f'{current_user.username} - {message}'},
         broadcast=True,
         room=int(data['channelId'])
         )


@socket.on('leave')
def leave(data):
    print('Client left')
    tokenObj = jwt.decode(data['authToken'], Configuration.SECRET_KEY)
    current_user = User.query.filter_by(id=tokenObj['user_id']).first()
    emit('message',
         {'msg': f'{current_user.username} has left the chat!'},
         broadcast=True,
         room=int(data['channelId'])
         )


@socket.on('disconnect')
def disconnect():
    print('Client disconnected')

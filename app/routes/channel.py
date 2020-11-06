from flask import Blueprint, request, jsonify
from app.models import User, Container, db
from ..config import Configuration
from ..util import token_required

bp = Blueprint('channel', __name__, url_prefix='/channel')


# RELOAD
@bp.route('/all')
@token_required
def get_channels(current_user):
    channels = Container.query.filter_by(is_channel=True).all()
    returnchannels = dict((channel.id, {
        'title': channel.title,
        'topic': channel.topic,
        'adminId': channel.admin_id,
        'users': channel.user_list
    }) for channel in channels)
    return {
        'data': returnchannels
    }


# CREATE CHANNEL
@bp.route('/', methods=['POST'])
@token_required
def create_channel(current_user):
    data = request.json
    title = data['title']
    new_channel = Container(
        admin=current_user,
        is_channel=True,
        title=f'#{title}',
        topic=data['topic'],
    )
    new_channel.members.append(current_user)
    db.session.add(new_channel)
    db.session.commit()
    channels = Container.query.filter_by(is_channel=True).all()
    returnchannels = dict((c.id, {
        'title': c.title,
        'topic': c.topic,
        'adminId': c.admin_id,
        'users': c.user_list
    }) for c in channels)
    return {
        'channels': returnchannels,
        'newChannelId': new_channel.id
    }

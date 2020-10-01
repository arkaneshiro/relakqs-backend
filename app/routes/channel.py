from flask import Blueprint, request
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
    }) for channel in channels)
    return {
        'data': returnchannels
    }


# JOIN CHANNEL
@bp.route('/<id>', methods=['POST'])
@token_required
def join_channel(current_user, id):
    channel = Container.query.filter_by(id=id).first()
    channel.members.append(current_user)
    db.session.commit()
    return {
        'data': current_user.container_list
    }


# LEAVE CHANNEL
@bp.route('/leave/<id>', methods=['DELETE'])
@token_required
def leave_channel(current_user, id):
    channel = Container.query.filter_by(id=id).first()
    channel.members.remove(current_user)
    db.session.commit()
    return {
        'data': current_user.container_list
    }


# EDIT TOPIC
@bp.route('/editTopic/<id>', methods=['PUT'])
@token_required
def edit_channel_topic(current_use, id):
    data = request.json
    channel = Container.query.filter_by(id=id).first()
    channel.topic = data['topic']
    db.session.commit()
    channels = Container.query.filter_by(is_channel=True).all()
    returnchannels = dict((c.id, {
        'title': c.title,
        'topic': c.topic,
        'adminId': c.admin_id,
    }) for c in channels)
    return {
        'data': returnchannels
    }

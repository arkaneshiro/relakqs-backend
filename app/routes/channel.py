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
    }) for channel in channels)
    return {
        'data': returnchannels
    }

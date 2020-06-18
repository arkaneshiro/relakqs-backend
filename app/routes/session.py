from flask import Blueprint, request
from werkzeug.security import generate_password_hash
from app.models import User, db
import jwt
from ..config import Configuration
from ..util import token_required

bp = Blueprint('session', __name__, url_prefix='/user')


# REGISTER
@bp.route('/', methods=['POST'])
def register_user():
    data = request.json

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        h_password=hashed_password,
        email=data['email'],
        bio=data['bio']
        )
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode({'user_id': new_user.id}, Configuration.SECRET_KEY)
    return {
        'authToken': token.decode('UTF-8'),
        'currentUserId': new_user.id,
        }


# LOGIN
@bp.route('/token', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user.check_password(data['password']):
        token = jwt.encode({'user_id': user.id}, Configuration.SECRET_KEY)
        return {
            'authToken': token.decode('UTF-8'),
            'currentUserId': user.id,
            }
    else:
        return {'message': 'Invalid credentials'}, 401


# TEST
@bp.route('/')
@token_required
def check_auth(current_user):
    return {'message': 'User is authorized!', 'user_id': current_user.id}


# @bp.route('/all')
# @token_required
# def get_all_users(current_user):
#     users = User.query.all()

#     users = {user.id: {'username': user.username, 'email': user.email}
#              for user in users}

#     return {'data': users}

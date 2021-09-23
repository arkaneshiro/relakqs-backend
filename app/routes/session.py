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
    user_by_username = User.query.filter_by(username=data['username']).first()
    user_by_email = User.query.filter_by(email=data['email']).first()
    if user_by_username:
        return {'message': 'Username already in use'}, 403
    elif user_by_email:
        return {'message': 'Email already in use'}, 403
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        h_password=hashed_password,
        email=data['email'],
        bio=data['bio']
        )
    db.session.add(new_user)
    db.session.commit()

    token = jwt.encode(
        {'user_id': new_user.id},
        Configuration.SECRET_KEY,
        algorithm="HS256")

    return {
        'authToken': token,
        'currentUserId': new_user.id,
        'username': new_user.username,
        'aviUrl': new_user.avi_url,
        'bio': new_user.bio,
        'containers': new_user.container_list,
        }


# LOGIN
@bp.route('/token', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return {'message': 'Invalid username or password'}, 401
    if user.check_password(data['password']):
        token = jwt.encode(
            {'user_id': user.id},
            Configuration.SECRET_KEY,
            algorithm="HS256")
        return {
            'authToken': token,
            'currentUserId': user.id,
            'username': user.username,
            'aviUrl': user.avi_url,
            'bio': user.bio,
            'containers': user.container_list,

            }
    else:
        return {'message': 'Invalid password'}, 401


@bp.route('/update', methods=['POST'])
@token_required
def update_user(current_user):
    data = request.json
    user = User.query.filter_by(id=current_user.id).first()
    if not data['bio']:
        print('no new bio')
        user.avi_url = data['aviUrl']
        db.session.commit()
        return {
            'aviUrl': user.avi_url
        }
    elif not data['aviUrl']:
        print('no new avi')
        user.bio = data['bio']
        db.session.commit()
        return {
            'bio': user.bio
        }
    else:
        print('new avi and bio')
        user.bio = data['bio']
        user.avi_url = data['aviUrl']
        db.session.commit()
        return {
            'bio': user.bio,
            'aviUrl': user.avi_url
        }


# RELOAD
@bp.route('/')
@token_required
def check_auth(current_user):
    user = User.query.filter_by(id=current_user.id).first()
    return {
        'username': user.username,
        'aviUrl': user.avi_url,
        'bio': user.bio,
        'containers': user.container_list,
    }

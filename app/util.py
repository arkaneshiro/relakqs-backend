import jwt
from flask import request
from .models import User
from functools import wraps
from .config import Configuration


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'a valid token is missing'}
        try:
            data = jwt.decode(token, Configuration.SECRET_KEY)
            current_user = User.query.filter_by(id=data['user_id']).first()
        except Exception:
            return {'message': 'token is invalid'}, 401
        return f(current_user, *args, **kwargs)
    return decorator

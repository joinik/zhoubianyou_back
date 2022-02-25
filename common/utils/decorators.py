from flask import g
from functools import wraps

def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        # 如果用户已登录，正常访问
        if g.user_id and not g.is_refresh:
            return f(*args, **kwargs)
        else:
            return {'message': 'Invalid Token', 'data': None}, 401

    return wrapper



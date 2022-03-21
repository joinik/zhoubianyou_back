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

# 权限验证
def permission_requeired(permission):
    def outter(func):
        @wraps(func)
        def inner(*args,**kwargs):
            user = g.zms_user
            if user is None:
                return {'message': 'Invalid Token', 'data': None}, 401
            # 判断用户是否具有访问权限
            if user.has_permission(permission):

                return func(*args,**kwargs)
            else:
                return {'message': 'Permission Denied', 'data': None}, 401
        return inner
    return outter


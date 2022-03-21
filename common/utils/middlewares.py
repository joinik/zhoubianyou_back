



from flask import request, g
from sqlalchemy.orm import load_only
from utils.my_jwt_util import verify_jwt

from app.models.user import User


def get_user():
    """获取用户信息"""

    # 获取请求头中的token
    auth = request.headers.get('Authorization')
    g.user_id = None     # 如果未登录， userid=None
    g.is_refresh = None  # 设置是否刷新token
    g.zms_user = None    # 用户对象
    if auth and auth.startswith('Bearer '):
        "提取token 0-6 被Bearer和空格占用 取下标7以后的所有字符"
        token = auth[7:]
        # 校验token
        data = verify_jwt(token)

        if data:    # 校验成功
            g.user_id = data.get('user_id')   # 如果已登录，  userid=2
            g.is_refresh = data.get('is_refresh')
            g.zms_user = User.query.options(load_only(User.id)).filter(User.id == g.user_id).first()





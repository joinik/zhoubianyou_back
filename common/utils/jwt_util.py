# -*- coding: utf-8 -*-
# author: JK time:2021/12/27
from datetime import datetime, timedelta

import jwt
from flask import current_app


def generate_jwt(payload, expiry, secret=None):
    """
    生成jwt
    :param payload:   dict 载荷
    :param expiry:    datetime 有效期
    :param secret:     密钥
    :return:   jwt
    """

    _payload = {'exp': expiry}
    _payload.update(payload)

    if not secret:
        secret = current_app.config['JWT_SECRET']

    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token.decode()


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """

    if not secret:
        secret = current_app.config['JWT_SECRET']

    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])

    except jwt.PyJWTError:
        payload = None

    return payload


def _generate_tokens(user_id,  need_refresh_token=True):

    # 生成业务token 2h有效期
    payload = {
        'user_id': user_id
    }

    # 有效期截止时间
    expiry = datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRE_HOURS'])

    # 调用 生成token
    token = generate_jwt(payload, expiry)

    # 生成refreshtoken 14天有效期
    refresh_payload = {
        'user_id': user_id,
        'is_refresh': True
    }

    refresh_token = None

    if  need_refresh_token:
        # 14天
        refresh_expiry = datetime.utcnow() + timedelta(days=current_app.config['JWT_EXPIRE_DAYS'])

        refresh_token = generate_jwt(refresh_payload, refresh_expiry)

    return token, refresh_token






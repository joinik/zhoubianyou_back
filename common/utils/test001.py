from datetime import datetime, timedelta

import jwt
from flask import current_app


def generate_jwt(payload, expiry, secret=None):
    _payload = {"exp": expiry}
    _payload.update(payload)

    if not secret:
        secret = current_app.config['JWT_SECRET']

    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token.decode()


def verify_jwt(token, secret=None):
    if not secret:
        secret = current_app.config['JWT_SECRET']
    try:
        payload = jwt.decode(token, secret,algorithms=['HS256'])

    except jwt.PyJWTError:
        payload = None
    return payload


def _generate_tokens(user_id, need_refresh_token=True):
    payload = {
        'user_id': user_id
    }

    expiry = datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRE_HOURS'])

    token = generate_jwt(payload, expiry)
    refresh_payload = {
        'user_id': user_id,
        "is_refresh": True
    }
    refresh_token = None

    if need_refresh_token:
        refresh_expiry = datetime.utcnow() + timedelta(days=current_app.config['JWT_EXPIRE_DAYS'])
        refresh_token = generate_jwt(refresh_payload, refresh_expiry)

    return token, refresh_token
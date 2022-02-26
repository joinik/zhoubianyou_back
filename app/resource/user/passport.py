import hashlib
from datetime import datetime

import random

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import redis_client, db
from app.models.user import User
from common.utils.constants import SMS_CODE_EXPIRE
from common.utils.my_jwt_util import _generate_tokens
from common.utils.my_parser import mobile_type, pwd_type


class SMSCodeResource(Resource):
    """获取短信验证码"""

    def get(self, mobile):
        # 随机生成短信验证码
        rand_num = '%06d' % random.randint(0, 999999)
        key = 'app:code:{}'.format(mobile)
        # 存入redis中
        redis_client.set(key, rand_num, ex=SMS_CODE_EXPIRE)

        # celery 第三方发送短信
        # celery_send_sms_code.delay(mobile, rand_num)
        print('>>>>>异步发送短信')
        print('短信验证码： "mobile": {}, "code": {}'.format(mobile, rand_num))
        return {'mobile': mobile}



class LoginResource(Resource):
    def post(self):
        # 构造请求参数
        parser = RequestParser()
        parser.add_argument('mobile', location='json', required=True, type=mobile_type)
        parser.add_argument('pwd', location='json', required=True, type=pwd_type)

        # 获取参数
        args = parser.parse_args()
        mobile = args.mobile
        pwd = args.pwd
        m = hashlib.sha256()
        m.update(pwd.encode('utf-8'))


        try:
            # 数据库查询
            user = User.query.options(load_only(User.id)).filter(User.mobile == mobile).first()
            if user:
                print('sdfd')
                print(user)
                if user.admini.password_hash != m.hexdigest():
                    return {"message": "账户或者密码有误"}, 401
                user.last_login = datetime.now()
                db.session.add(user)
                db.session.commit()
                # 生成jwt
                token, refresh_token = _generate_tokens(user.id)
                return {'token': token, 'refresh_token': refresh_token}, 201

            else:
                return {'message': "没有权限，非法登录", "data": None}, 401

        except Exception as e:
            print('登录 数据库查询失败')
            print(e)
            return {'message': "请重新登录", "data":None}, 401




    def put(self):
        if g.is_refresh:
            token, refresh_token = _generate_tokens(g.user_id, False)
            return {'token': token}, 201
        else:
            return {'message': "Invalid refreshToken", 'data': None}, 403
















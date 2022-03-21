import hashlib
from datetime import datetime

import random

from flask_restful import Resource
from flask_restful.inputs import regex
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import redis_client, db
from app.models.user import User, Administrator
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
        print('周边游注册码： "mobile": {}, "code": {}'.format(mobile, rand_num))
        return {'mobile': mobile}




class RegisterResource(Resource):
    """管理员注册视图"""
    def post(self):
        # 构造请求参数
        parser = RequestParser()
        parser.add_argument('mobile', location='json', required=True, type=mobile_type)
        parser.add_argument('pwd', location='json', required=True, type=pwd_type)
        parser.add_argument('register_code', location='json', required=True, type=regex(r'^\d{6}$'), help='注册验证码错误')
        # 获取参数
        args = parser.parse_args()
        mobile = args.mobile
        pwd = args.pwd
        code = args.register_code

        # 校验短信验证码
        # key = 'app:code:{}'.format(mobile)
        # real_code = redis_cluster.get(key)
        # if not real_code or real_code != vcode:
        #     return {'message': 'Invalid Code', 'data': None}, 400


        # 存入数据库
        # 1.存入用户表
        user = User(nick_name=mobile,mobile=mobile)
        # print(user)
        user.password = pwd
        db.session.add(user)
        db.session.flush()
        # 2.存入管理员表

        admini = Administrator(account_id=user.id,group_id=2)

        db.session.add(admini)
        db.session.commit()

        return {"message": "OK", "admini_id":admini.admini_id},201


class LoginResource(Resource):
    """登录视图"""
    def post(self):
        # 构造请求参数
        parser = RequestParser()
        parser.add_argument('mobile', location='json', required=True, type=mobile_type)
        parser.add_argument('pwd', location='json', required=True, type=pwd_type)

        # 获取参数
        args = parser.parse_args()
        mobile = args.mobile
        pwd = args.pwd

        # 自己的做的加密方式
        # m = hashlib.sha256()
        # m.update(pwd.encode('utf-8'))



        try:
            # 数据库查询
            user = User.query.options(load_only(User.id)).filter(User.mobile == mobile).first()

            if user.roles:
                if not user.check_password(pwd):
                    return {"message": "账户或者密码有误"}, 401
                user.last_login = datetime.now()
                db.session.add(user)
                db.session.commit()
                # 生成jwt
                token, refresh_token = _generate_tokens(user.id)
                return {'token': token, 'refresh_token': refresh_token}, 201

            else:
                return {"message": "没有权限，非法登录", "data": None}, 401

        except Exception as e:
            print('登录 数据库查询失败')
            print(e)
            return {"message": "请重新登录", "data":None}, 401




    def put(self):
        if g.is_refresh:
            token, refresh_token = _generate_tokens(g.user_id, False)
            return {"token": token}, 201
        else:
            return {'message': "Invalid refreshToken", 'data': None}, 403




















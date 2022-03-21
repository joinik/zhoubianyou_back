from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import db
from app.models.user import User, RoleGroup
from common.utils.decorators import login_required, permission_requeired
from common.utils.my_parser import flag_parser


class UserManage(Resource):
    method_decorators = [login_required, permission_requeired(RoleGroup.ZMSPermission.ZMSUSER)]

    def get(self):
        """查询所有普通用户"""
        user_list = User.query.options(load_only(User.id)).filter(User.password_hash.is_(None)).all()
        rest = [
            {"id": item.id,
             "name": item.nick_name,
             "mobile": item.mobile,
             "business": item.business,
             "status": item.status}
            for item in user_list
        ]

        return {"message": "OK", "data": rest}


    def put(self):
        """修改用户的状态"""

        parser = RequestParser()

        parser.add_argument('user', location='json', required=True, type=int, action='append')
        parser.add_argument('flag', location='json', required=True, type=flag_parser)
        parser.add_argument('action', location='json', type=str)

        # 获取参数
        args = parser.parse_args()
        user_list = args.user  # 用户的id
        action = args.action  # 是否批量处理
        flag = args.flag  # 是封禁还是解封

        # 判断是否进行批量处理
        if action == 'true':
            if flag == 'banned':
                print('封禁')
                rest = []
                for user_id in user_list:
                    try:
                        user = User.query.options(load_only(User.id)).filter(User.id == user_id).first()
                        user.status = 0
                        rest.append(user)
                    except Exception as e:
                        print("查询用户id失败")
                        print(e)
                        return {"message": "Invalid Operate"}, 400

                db.session.add_all(rest)
                db.session.commit()

                rest_list = [{"id": item.id,
                              "name": item.nick_name,
                              "mobile": item.mobile,
                              "business": item.business,
                              "status": item.status}
                             for item in rest]

                return {"message": "OK", "data": rest_list}

            else:
                # 解禁
                print('解禁')
                rest = []
                for user_id in user_list:
                    try:
                        user = User.query.options(load_only(User.id)).filter(User.id == user_id).first()
                        user.status = 1
                        rest.append(user)
                    except Exception as e:
                        print("查询用户id失败")
                        print(e)
                        return {"message": "Invalid Operate"}, 400

                db.session.add_all(rest)
                db.session.commit()
                rest_list = [{"id": item.id,
                              "name": item.nick_name,
                              "mobile": item.mobile,
                              "business": item.business,
                              "status": item.status}
                             for item in rest]
                return {"message": "OK", "data": rest_list}, 201

        else:
            # 不是批量处理
            if flag == "banned":
                try:
                    user = User.query.options(load_only(User.id)).filter(User.id == user_list[0]).first()
                    user.status = 0
                    db.session.add(user)
                    db.session.commit()

                except Exception as e:
                    print("查询用户id失败")
                    print(e)
                    return {"message": "Invalid Operate"}, 400

                rest = {"id": user.id,
                        "name": user.nick_name,
                        "mobile": user.mobile,
                        "business": user.business,
                        "status": user.status}
                return {"message": "OK", "data": rest}
            else:
                try:
                    user = User.query.options(load_only(User.id)).filter(User.id == user_list[0]).first()
                    user.status = 1
                    db.session.add(user)
                    db.session.commit()
                except Exception as e:
                    print("查询用户id失败")
                    print(e)
                    return {"message": "Invalid Operate"}, 400

                rest = {"id": user.id,
                        "name": user.nick_name,
                        "mobile": user.mobile,
                        "business": user.business,
                        "status": user.status}

                return {"message": "OK", "data": rest}

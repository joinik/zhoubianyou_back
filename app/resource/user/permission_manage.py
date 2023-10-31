from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy import and_
from sqlalchemy.orm import load_only

from app import db
from app.models.user import RoleGroup, User, Administrator
from common.utils.decorators import login_required, permission_requeired


class AdminPermission(Resource):
    """后台用户权限管理类"""
    method_decorators = [login_required, permission_requeired(RoleGroup.ZMSPermission.ADMINER)]

    def get(self):
        parser = RequestParser()
        parser.add_argument('page', default=0, location='args', type=int)
        parser.add_argument('limit', default=10, location='args', type=int)
        args = parser.parse_args()
        page = args.page
        limit = args.limit
        user_id = g.user_id
        paginate = User.query.options(load_only(User.id)).\
            filter(and_(User.id != 8, User.id != user_id), User.password_hash.isnot(None)).\
            paginate(page=page,per_page=limit, error_out=False)


        #
        rest = []
        for item in paginate.items:
            user = {}
            role = item.roles[0]
            user["permission"] = {"role_id": role.role_id, "per_name": role.role_name, "per_level": role.permissions}
            user["user_id"] = item.id
            user["nick_name"] = item.nick_name
            user["mobile"] = item.mobile
            user["ctime"] = item.ctime.isoformat()
            rest.append(user)
        return {"totalPage": paginate.pages, "rest": rest}


    def put(self):
        """修改权限"""

        parser = RequestParser()
        parser.add_argument('user_id', required=True, location='json', type=int)
        parser.add_argument('per_id', required=True, location='json', type=int)
        args = parser.parse_args()
        user_id = args.user_id
        per_id = args.per_id

        try:
            # 根据id 修改权限
            user = User.query.options(load_only(User.id)).filter(User.id == user_id).first()
            admin = Administrator.query.options(load_only(Administrator.admini_id)).\
                filter(Administrator.account_id == user.id).update({"group_id": per_id})

            # 提交到数据库
            db.session.commit()
            if admin:
                rest = {}
                role = user.roles[0]
                rest["permission"] = {"role_id": role.role_id, "per_name": role.role_name, "per_level": role.permissions}
                rest["user_id"] = user.id
                rest["nick_name"] = user.nick_name
                rest["mobile"] = user.mobile
                rest["ctime"] = user.ctime.isoformat()

                return rest

        except Exception as e:
            print("修改权限 失败")
            print(e)
            return {"message": "修改权限 失败"}, 400


class PermissionResource(Resource):
    """权限管理类"""
    method_decorators = {"post": [login_required, permission_requeired(RoleGroup.ZMSPermission.ALL_PERMISSION)]}

    def get(self):
        """查询权限"""
        parser = RequestParser()
        parser.add_argument('page', default=0, location='args', type=int)
        parser.add_argument('limit', default=10, location='args', type=int)
        args = parser.parse_args()
        page = args.page
        limit = args.limit

        paginate = RoleGroup.query.options(load_only(RoleGroup.role_id)).\
            paginate(page=page, per_page=limit, error_out=False)

        rest = [
            item.to_dict() for item in paginate.items
        ]

        return {"totalPage": paginate.pages, "rest": rest}
from flask_restful import Resource
from sqlalchemy.orm import load_only

from app.models.user import User, RoleGroup
from common.utils.decorators import login_required, permission_requeired


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


#     def post(self):
#         """修改用户的状态"""
#         parser
# parser = RequestParser()
#         parser.add_argument('mobile', location='json', required=True, type=mobile_type)
#         parser.add_argument('pwd', location='json', required=True, type=pwd_type)

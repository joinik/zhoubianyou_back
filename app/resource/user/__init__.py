from flask import Blueprint
from flask_restful import Api
from .passport import LoginResource, RegisterResource
from utils.constants import BASE_URL_PRIFIX

# 1.创建蓝图对象
# from .profile import CurrentUserResource, UserPhotoResource, UserInfoResource
# from .router_card import TravelCardResource, WeatherResource
from .permission_manage import AdminPermission, PermissionResource
from .user_manage import UserManage

user_bp = Blueprint('user', __name__, url_prefix=BASE_URL_PRIFIX)

# 2.创建Api对象
user_api = Api(user_bp)

from utils.my_output import output_json

user_api.representation('application/json')(output_json)


# 手机号方式登录
user_api.add_resource(LoginResource, '/login')
user_api.add_resource(RegisterResource, '/register')
user_api.add_resource(UserManage, '/user')
user_api.add_resource(AdminPermission, '/userPermission')
user_api.add_resource(PermissionResource, '/permission')


from flask import Blueprint
from flask_restful import Api
from .passport import LoginResource
from utils.constants import BASE_URL_PRIFIX

# 1.创建蓝图对象
# from .profile import CurrentUserResource, UserPhotoResource, UserInfoResource
# from .router_card import TravelCardResource, WeatherResource

user_bp = Blueprint('user', __name__, url_prefix=BASE_URL_PRIFIX)

# 2.创建Api对象
user_api = Api(user_bp)

from utils.my_output import output_json

user_api.representation('application/json')(output_json)

# 3.添加类视图
# user_api.add_resource(UsernameResource, '/usernames/<uname:username>')
# 手机号方式登录
user_api.add_resource(LoginResource, '/login')

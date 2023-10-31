from flask import Blueprint
from flask_restful import Api

from utils.constants import BASE_URL_PRIFIX

# 1.创建蓝图对象
# from .profile import CurrentUserResource, UserPhotoResource, UserInfoResource
# from .router_card import TravelCardResource, WeatherResource
from app.resource.comment.com_manage import CommentManageResource

comment_bp = Blueprint('comment', __name__, url_prefix=BASE_URL_PRIFIX)

# 2.创建Api对象
comment_api = Api(comment_bp)

from utils.my_output import output_json

comment_api.representation('application/json')(output_json)

comment_api.add_resource(CommentManageResource, '/comment')


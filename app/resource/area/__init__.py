from flask import Blueprint
from flask_restful import Api

from utils.constants import BASE_URL_PRIFIX

from app.resource.area.views import AreaProvinceResource, SubsResource

area_bp = Blueprint('area', __name__, url_prefix=BASE_URL_PRIFIX)

# 2.创建Api对象
area_api = Api(area_bp)


# 设置json包装格式
from utils.my_output import output_json
area_api.representation('application/json')(output_json)

# 添加类视图
area_api.add_resource(AreaProvinceResource, '/areas')
area_api.add_resource(SubsResource, '/areas/<int:pk>')


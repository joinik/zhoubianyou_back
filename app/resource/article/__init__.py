from flask import Blueprint
from flask_restful import Api

from utils.constants import BASE_URL_PRIFIX

# 1.创建蓝图对象
from app.resource.article.art_manage import SpecialArticleResource

art_bp = Blueprint('article', __name__, url_prefix=BASE_URL_PRIFIX)

# 2.创建Api对象
art_api = Api(art_bp)

from utils.my_output import output_json

art_api.representation('application/json')(output_json)

# 3.添加类视图

art_api.add_resource(SpecialArticleResource, '/spe') # 特色



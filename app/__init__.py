


from flask import Flask
from os.path import *
import sys
from flask_cors import CORS


from flask_migrate import Migrate

from app.settings.config import config_dict

#  将common路径加入模块查询路径
BASE_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0,BASE_DIR + '/common')

from utils.constants import EXTRA_ENV_CONFIG


def create_flask_app(type):
    """创建flask应用"""

    # 创建flask应用
    app = Flask(__name__)
    # 配置跨域
    CORS(app, supports_credentials=True)

    # 根据类型加载配置子类
    config_class = config_dict[type]

    # 先加载默认配置
    app.config.from_object(config_class)

    # 在加载额外配置
    app.config.from_envvar(EXTRA_ENV_CONFIG, silent=True)

    # 返回应用
    return app


from flask_sqlalchemy import SQLAlchemy

# # sqlalchemy 组件对象
db = SQLAlchemy()


def register_extensions(app):
    """组件初始化"""

    # sqlalchemy组件初始化
    from app import db
    db.init_app(app)

    # 数据迁移组件初始化
    Migrate(app, db)

    # 添加转换器
    from utils.my_converters import register_converters
    register_converters(app)

    # 添加请求钩子
    from utils.middlewares import get_user
    app.before_request(get_user)


def register_bp(app:Flask):
    """注册蓝图"""
    # from app.resource.user import user_bp # 进行局部导入，避免组件没有初始化完成
    # from app.resource.article import article_bp
    # from app.resource.area import area_bp
    # from app.resource.comment import comment_bp
    # app.register_blueprint(user_bp)
    # app.register_blueprint(article_bp)
    # app.register_blueprint(area_bp)
    # app.register_blueprint(comment_bp)

def create_app(type):
    """创建应用 和组件初始化"""
    app = create_flask_app(type)

    # 组件初始化
    register_extensions(app)

    # 注册蓝图
    register_bp(app)

    return app


import calendar
from datetime import datetime, date, timedelta

from sqlalchemy import or_
from sqlalchemy.orm import load_only

from app import create_app, db
from flask import jsonify, request, g

# 创建web应用
from app.models.article import Article, Classes
from app.models.user import RoleGroup, User

app = create_app('dev')




import re

def handle_data(img_url):
    # 处理 img_url
    st = re.sub(r'^http://.*?hn',"http://ra1r2qeyc.hd", img_url)
    return st




@app.route('/handle')
def mysql_handle():
    # 特色查询
    art_li = Article.query.options(load_only(Article.art_id)).filter(Article.cover.isnot(None)).all()

    for item in art_li:
        cover_dict = {}
        cover = item.cover
        for k, v in cover.items():
            cover_dict[k] = handle_data(v)
        # print(cover)
        item.cover = cover_dict

    # db.session.add_all(art_li)
    # db.session.commit()

    # spe_li = Special.query.options(load_only(Special.id)).filter(Special.intr_photo.isnot(None), Special.story_photo.isnot(None)).all()
    #
    # for item in spe_li:
    #     if item.intr_photo:
    #         intr_dict = {}  # 地区介绍
    #         cult_dict = {}  # 地区文化
    #         scen_dict = {}  # 地区美景
    #         snack_dict = {} # 地区美食
    #         for k,v in item.intr_photo.items():
    #             intr_dict[k] = handle_data(v)
    #         for k, v in item.cultural_photo.items():
    #             cult_dict[k] = handle_data(v)
    #         for k, v in item.scenery_photo.items():
    #             scen_dict[k] = handle_data(v)
    #         for k, v in item.snack_photo.items():
    #             snack_dict[k] = handle_data(v)
    #         item.intr_photo = intr_dict
    #         item.cultural_photo = cult_dict
    #         item.scenery_photo = scen_dict
    #         item.snack_photo = snack_dict
    #
    #     if item.story_photo:
    #         story_dict = {}  # 用户故事
    #         for k,v in item.story_photo.items():
    #             story_dict[k] = handle_data(v)
    #         item.story_photo = story_dict

    # db.session.add(art_li,spe_li)
    db.session.commit()
        # print(item.to_dict())
        # input('dnggg>>>>>>>>>>>>')



    # cat_model = Category.query.options(load_only(Category.id)).filter(Category.is_deleted == 0).all()
    #
    # rest = []
    # for item in cat_model:
    #     art = [item.to_dict() for item in item.articles.limit(5).all()]
    #     rest.append({item.cate_name: art})
    # # input('等待')

    return jsonify({"message": "OK"})

@app.route('/')
def route_map():
    """定义根路由: 获取所有路由规则"""
    # # 2. 运营角色（修改个人个人信息，管理帖子，管理评论，管理前台用户）
    # operator = RoleGroup.query.filter(RoleGroup.role_name=='运营').first()
    # operator.permissions = RoleGroup.ZMSPermission.ANNOUNCE | RoleGroup.ZMSPermission.POSTER | RoleGroup.ZMSPermission.COMMENTER | RoleGroup.ZMSPermission.BOARDER
    # #
    # 3. 管理员（拥有绝大部分权限）
    # admin = RoleGroup.query.filter(RoleGroup.role_name=='管理员').first()
    # admin.permissions = RoleGroup.ZMSPermission.ANNOUNCE | RoleGroup.ZMSPermission.POSTER | RoleGroup.ZMSPermission.COMMENTER | RoleGroup.ZMSPermission.BOARDER | RoleGroup.ZMSPermission.ZMSUSER
    #
    # #
    # # # 4. 开发者
    # developer = RoleGroup.query.filter(RoleGroup.role_name=='开发者').first()
    # developer.permissions = RoleGroup.ZMSPermission.ALL_PERMISSION

    # vip_admin = RoleGroup(role_name='超级管理员', desc='管理权限,管理管理员,本系统所有权限')
    # vip_admin.permissions = RoleGroup.ZMSPermission.ANNOUNCE | RoleGroup.ZMSPermission.POSTER | RoleGroup.ZMSPermission.COMMENTER | RoleGroup.ZMSPermission.BOARDER | RoleGroup.ZMSPermission.ZMSUSER | RoleGroup.ZMSPermission.ADMINER
    # # db.session.add_all([operator, admin, developer])
    # db.session.add(vip_admin)
    # db.session.commit()


    # 获取当前时间日期
    to_y = datetime.today()
    year = to_y.year
    month = to_y.month

    # monthrange(year, month)：返回指定年月，由第一天所在的星期和本月的总天数组成的元组。
    x, y = calendar.monthrange(year, month)
    # 明天的日期
    next_day = date.today() + timedelta(days=1)
    # print(next_day)

    # 本月的第一天，最后一天
    first_day = date.today().replace(day=1)
    last_day = date(year=year, month=month, day=y)
    # print(first_day, last_day)

    # print('时间列表')
    month_list = [date.today() + timedelta(days=-i) for i in range(0, 32, 4)]
    month_list = list(reversed(month_list))
    # 日期对象转成字符串转换函数
    def to_day_str(item):
        return item.strftime("%Y-%m-%d")

    rest_month_list = [ to_day_str(item) for item in month_list]
    # print(rest_month_list)
    # print(datetime.now().minusDays(1))
    # print(date.today())
    # 日发游记数
    day_post_youji = Article.query.options(load_only(Article.art_id)).filter(Article.classes_id == 6, Article.ctime >= date.today(),
                                                            Article.ctime < next_day).count()

    # 获取总用户数量
    user_count = User.query.options(load_only(User.id)).filter(User.password_hash.is_(None)).count()
    # 获取日活用户
    day_live_user_count = User.query.options(load_only(User.id)).filter(User.password_hash.is_(None),
                                                                        db.cast(User.last_login, db.DATE) == db.cast(
                                                                            datetime.now(), db.DATE)).count()
    # 获取日增用户
    day_create_user_count = User.query.options(load_only(User.id)).filter(User.password_hash.is_(None),
                                                                          User.ctime >= date.today(),
                                                                          User.ctime < next_day).count()
    # 获取月活用户
    month_live_user = User.query.options(load_only(User.id)).filter(User.password_hash.is_(None),
                                                                    or_(User.last_login >= first_day,
                                                                        User.last_login < last_day)).all()
    month_live_user_list = [item.id for item in month_live_user]

    # 分类下的文章数量
    huati = Article.query.options(load_only(Article.art_id)).filter(Article.classes_id == 1).count()
    qiuzhu = Article.query.options(load_only(Article.art_id)).filter(Article.classes_id == 2).count()
    huodong = Article.query.options(load_only(Article.art_id)).filter(Article.classes_id == 3).count()
    gonggao = Article.query.options(load_only(Article.art_id)).filter(Article.classes_id == 4).count()
    shangjia = Article.query.options(load_only(Article.art_id)).filter(Article.classes_id == 5).count()
    youji = Article.query.options(load_only(Article.art_id)).filter(Article.classes_id == 6).count()

    class_list = Classes.query.options(load_only(Classes.id)).limit(6).all()
    rest_class_list = [item.cla_title for item in class_list]

    return jsonify({"data": {"user_count": user_count,
                             "day_post_youji": day_post_youji,
                             "day_live_user_count": day_live_user_count,
                             "day_create_user_count": day_create_user_count,
                             "month_user": {"month_live_user_list": month_live_user_list, "rest_month_list": rest_month_list},
                             "class_art": {"rest_class_list": rest_class_list, "art_num": [huati,qiuzhu,huodong,gonggao,shangjia,youji]}
                             }})

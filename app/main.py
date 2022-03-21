


from sqlalchemy.orm import load_only

from app import create_app, db
from flask import jsonify, request, g


# 创建web应用
from app.models.user import RoleGroup

app = create_app('dev')



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
    #
    # db.session.add_all([operator, admin, developer])
    # # db.session.add(admin)
    # db.session.commit()
    return jsonify({rule.endpoint: rule.rule for rule in app.url_map.iter_rules()})





from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from common.utils.my_time_model import TimeBaseModel





class Administrator(db.Model):
    """管理员类"""
    __tablename__ = 'tb_administrator'
    admini_id = db.Column(db.Integer, primary_key=True, doc='管理员ID')
    account_id = db.Column(db.Integer, db.ForeignKey('tb_user_basic.id'), doc='用户ID')
    group_id = db.Column(db.Integer, db.ForeignKey("tb_role_group.role_id"), doc='角色id')




class RoleGroup(db.Model,TimeBaseModel):


    class ZMSPermission(object):
        # 255的二进制方式来表示 1111 1111
        # 0. 超级管理员(开发者)权限
        ALL_PERMISSION = 0b11111111
        # 1. 发布公告、特色权限
        ANNOUNCE = 0b00000001
        # 2. 管理文章权限
        POSTER = 0b00000010
        # 3. 管理评论的权限
        COMMENTER = 0b00000100
        # 4. 管理文章分类的权限
        BOARDER = 0b00001000
        # 5. 管理后台用户的权限
        ZMSUSER = 0b00010000
        # 6. 管理后台管理员的权限
        ADMINER = 0b00100000

    """权限分组类"""
    __tablename__ = 'tb_role_group'
    role_id = db.Column(db.Integer, primary_key=True, doc='角色ID')
    role_name = db.Column(db.String(20), unique=True, doc='角色昵称')
    desc = db.Column(db.String(200), nullable=True, doc='描述信息')
    permissions = db.Column(db.Integer, default=ZMSPermission.ANNOUNCE)
    # 定义关系,users,roles,分别是两个表对应哪个的字段，secondary指定中间表
    users = db.relationship('User', secondary=Administrator.__tablename__,
                            backref=db.backref('roles'))











class User(db.Model):
    """用户基本信息"""

    __tablename__ = 'tb_user_basic'

    id = db.Column(db.Integer, primary_key=True, doc='用户ID')
    nick_name = db.Column(db.String(20), unique=True, doc='昵称')
    mobile = db.Column(db.String(11), unique=True, nullable=False, doc='手机号')
    avatar = db.Column(db.String(256), doc='用户头像')
    last_login = db.Column(db.DateTime, default=datetime.now, doc='最后登录的时间')
    ctime = db.Column(db.DateTime, default=datetime.now, doc='注册时间')
    intr = db.Column(db.String(128), doc='简介')
    status = db.Column(db.Integer, default=1, doc='状态，是否可用，0-不可用，1-可用')
    business = db.Column(db.Integer, default=0, doc='认证，是否为商家，0不是，1-是')
    dianzan_num = db.Column(db.Integer, default=0, doc='获赞总数')
    travel_note_num = db.Column(db.Integer, default=0, doc='游记总数')
    note_num = db.Column(db.Integer, default=0, doc='发帖总数')
    dianliang_area_num = db.Column(db.Integer, default=0, doc='点亮地区数')
    last_area_id = db.Column(db.Integer, db.ForeignKey("tb_area.id"), doc='用户上次位置')
    last_area = db.relationship("Area", backref=db.backref('users', uselist=False), uselist=False)
    password_hash = db.Column(db.String(128))  # 加密的密码



    def to_dict(self):
        """模型转字典, 用于序列化处理"""
        return {
            'id': self.id,
            'name': self.nick_name,
            'mobile': self.mobile,
            'photo': self.avatar,
            'intro': self.intr,
            'dianzan_count': self.dianzan_num,
            'note_num_count': self.note_num,
            'travel_note_count': self.travel_note_num,
            'dianliang_area_count': self.dianliang_area_num,
            'business': self.business,
            'last_address': self.last_area.area_name if self.last_area else None,
            # 'like_comments': self.like_comments.
        }

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, pwd):
        # 加密
        print("密码",pwd)
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, raw_password):
        # 原始密码和加密后的密码是否一致
        result = check_password_hash(self.password_hash, raw_password)
        return result


    @property
    def permissions(self):

        # 没有任何权限
        if not self.roles:
            return 0
        all_permissions = 0
        # 遍历权限
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
        return all_permissions
        # 判断用户权限

    def has_permission(self, permission):
        # all_permissions = self.permissions
        # result =  all_permissions & permission == permission
        # return result
        return self.permissions & permission == permission

        # 判断是否为开发者

    def is_developer(self):
        return self.has_permission(RoleGroup.ZMSPermission.ALL_PERMISSION)


class Address(db.Model, TimeBaseModel):
    """地址表"""

    __tablename__ = "tb_address"


    id = db.Column(db.Integer, primary_key=True, doc='地址ID')
    addr_title = db.Column(db.String(20), doc='地址名称')
    province_id = db.Column(db.Integer, db.ForeignKey("tb_area.id"), doc='省')
    city_id = db.Column(db.Integer, db.ForeignKey("tb_area.id"), doc='市')
    district_id = db.Column(db.Integer, db.ForeignKey("tb_area.id"), doc='区')
    place = db.Column(db.String(50), doc='地址')
    id_deleted = db.Column(db.Boolean, default=False, doc='逻辑删除')


class UserProfile(db.Model, TimeBaseModel):
    """用户资料表"""
    __tablename__ = 'tb_user_profile'


    user_id = db.Column(db.Integer, db.ForeignKey("tb_user_basic.id"), primary_key=True, doc='用户ID')
    email = db.Column(db.String(20), doc='邮箱')
    gender = db.Column(db.Integer, default=1, doc='性别，1 男，2 女')
    age = db.Column(db.Integer, doc='年龄')
    default_address_id = db.Column(db.Integer, db.ForeignKey("tb_address.id"), nullable=True, doc='用户常住地址')
    default_address = db.relationship("Address", backref=db.backref('users_profile', uselist=False), uselist=False)
    user_basic = db.relationship("User", backref=db.backref('user_profile', uselist=False), uselist=False)

    def to_dict(self):
        return {
            "id": self.user_id,
            'name': self.user_basic.nick_name,
            "email": self.email,
            "gender": self.gender,
            "age": self.age,
            "default_address": self.default_address_id
        }




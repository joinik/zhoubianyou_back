


from datetime import datetime

from app import db
from common.utils.my_time_model import TimeBaseModel



class RoleGroup(db.Model,TimeBaseModel):
    """权限分组类"""
    __tablename__ = 'tb_role_group'
    role_id = db.Column(db.Integer, primary_key=True, doc='角色ID')
    role_name = db.Column(db.String(20), unique=True, doc='角色昵称')


class Administrator(db.Model):
    __tablename__ = 'tb_administrator'
    admini_id = db.Column(db.Integer, primary_key=True, doc='管理员ID')
    account_id = db.Column(db.Integer, db.ForeignKey('tb_user_basic.id'), doc='用户ID')
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    group_id = db.Column(db.Integer, db.ForeignKey("tb_role_group.role_id"), doc='角色id')
    account = db.relationship("User", backref=db.backref('admini', uselist=False), uselist=False)

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




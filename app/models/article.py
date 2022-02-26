from datetime import datetime

from app import db
from common.utils.my_time_model import TimeBaseModel


class Classes(db.Model, TimeBaseModel):
    """文章分类"""
    __tablename__ = "tb_classes"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    cla_title = db.Column(db.String(64), nullable=False)  # 分类名
    is_deleted = db.Column(db.Boolean, default=False, doc='逻辑删除')


class Article(db.Model, TimeBaseModel):
    """文章基本信息表"""
    __tablename__ = 'tb_article_basic'

    class STATUS:
        DRAFT = 0  # 草稿
        UNREVIEWED = 1  # 待审核
        APPROVED = 2  # 审核通过
        FAILED = 3  # 审核失败
        DELETED = 4  # 已删除
        BANNED = 5  # 封禁

    art_id = db.Column(db.Integer, primary_key=True, doc='文章ID')
    user_id = db.Column(db.Integer, db.ForeignKey("tb_user_basic.id"), doc='用户ID')
    classes_id = db.Column(db.Integer, db.ForeignKey("tb_classes.id"), doc='分类ID')
    area_id = db.Column(db.Integer, db.ForeignKey('tb_area.id'), doc='地区ID')

    art_title = db.Column(db.String(128), doc='文章标题')
    cover = db.Column(db.JSON, doc='封面')
    status = db.Column(db.Integer, default=2, doc='文章状态')
    reason = db.Column(db.String(256), doc='未通过原因')
    check_id = db.Column(db.Integer, db.ForeignKey('tb_user_basic.id'), doc='审核人员ID')
    check_time = db.Column(db.DateTime, doc='审核时间')
    delete_time = db.Column(db.DateTime, doc='删除时间')
    comment_count = db.Column(db.Integer, default=0, doc='评论数')
    like_count = db.Column(db.Integer, default=0, doc='点赞数')
    dislike_count = db.Column(db.Integer, default=0, doc='点踩数')

    # area = db.relationship("Area", backref=db.backref('articles', lazy='dynamic'), uselist=False)
    user = db.relationship("User", backref=db.backref('articles', lazy='dynamic'), foreign_keys=[user_id], uselist=False)
    classes = db.relationship('Classes', backref=db.backref('articles', lazy='dynamic'), uselist=False)
    area = db.relationship('Area', backref='articles', uselist=False)

    # # 当前新闻的所有评论
    comments = db.relationship("Comment", backref=db.backref('article', uselist=False), lazy="dynamic")
    article_content = db.relationship("ArticleContent",
                                      backref=db.backref('articles', uselist=False), uselist=False)

    def to_dict(self):
        return {
            'area_id': self.area.id,
            'area_name': self.area.area_name,
            'art_id': self.art_id,
            'title': self.art_title,
            "cover": self.cover if self.cover else None,
            'pubdate': self.ctime.isoformat(),
            'update': self.utime.isoformat(),
            'aut_id': self.user.id,
            'aut_name': self.user.name,
            'aut_photo': self.user.profile_photo,
            'content': self.article_content.content,
            'comment_count': self.comment_count,
            'like_count': self.like_count,
            'dislike_count': self.dislike_count
        }


class ArticleContent(db.Model):
    """
    文章内容表
    """
    __tablename__ = 'tb_article_content'

    # __table_args__ = {'extend_existing': True}
    # extend_existing = True
    article_id = db.Column(db.Integer, db.ForeignKey("tb_article_basic.art_id"), primary_key=True, doc='文章ID')
    content = db.Column(db.Text, doc='帖文内容')


class ArticleReport(db.Model):
    """
    文章举报表
    """
    __tablename__ = 'tb_article_report'
    class TYPE:
        OTHERPROBLEMS: 0  # 其他问题
        TITLEEXAGGERATE: 1  # 标题夸张
        VULGARPORN: 2  # 低俗色情
        WRONGLY: 3  # 错别字多
        ARCHIVEDNEWSREPEAT: 4  # 旧闻重复
        BLINDADVERTISING: 5  # 广告软文
        NOTREALCONTENT: 6  # 内容不实
        CRIMINAL: 7  # 涉嫌违法犯罪
        TORT: 8  # 侵权

    report_id = db.Column(db.Integer, primary_key=True, doc='主键id')
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user_basic.id'), doc='用户id')
    article_id = db.Column(db.Integer, db.ForeignKey('tb_article_basic.art_id'), doc='文章id')
    type = db.Column(db.Integer, doc='类型，0-其他问题，1-标题夸张，2-低俗色情，3-错别字多，4-旧闻重复，5-广告软文，6-内容不实，7-涉嫌违法犯罪，8-侵权')
    remark = db.Column(db.String(256), doc='备注问题')
    ctime = db.Column(db.DateTime, default=datetime.now, doc='创建时间')


class Special(db.Model,TimeBaseModel):
    """特色类"""
    __tablename__ = 'tb_special'

    id = db.Column(db.Integer,primary_key=True,doc='特色主键')
    spe_intr = db.Column(db.String(256), doc='当地介绍')
    spe_cultural = db.Column(db.String(256), doc='文化特色')
    spe_scenery = db.Column(db.String(256), doc='美丽景色')
    spe_snack = db.Column(db.String(256),doc='特色小吃')
    area_id = db.Column(db.Integer, db.ForeignKey('tb_area.id'), doc='地区ID')
    cover = db.Column(db.JSON, doc='封面')
    admini_id = db.Column(db.Integer, db.ForeignKey('tb_administrator.admini_id'), doc='管理员id')


    def todict(self):
        return {
            "area_id": self.area_id,
            "spe_intr": self.spe_intr,
            "spe_cultural": self.spe_cultural,
            "spe_scenery": self.spe_scenery,
            "spe_snack": self.spe_snack,
            "cover": self.cover if self.cover else None
        }





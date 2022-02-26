from datetime import datetime

from app import db


class Comment(db.Model):
    """
    文章评论
    """
    __tablename__ = 'tb_article_comment'


    class STATUS:
        UNREVIEWED = 0  # 待审核
        APPROVED = 1  # 审核通过
        FAILED = 2  # 审核失败
        DELETED = 3  # 已删除

    com_id = db.Column(db.Integer, primary_key=True, doc='评论ID')
    user_id = db.Column(db.Integer, db.ForeignKey("tb_user_basic.id"),nullable=False, doc='用户ID')
    article_id = db.Column(db.Integer, db.ForeignKey("tb_article_basic.art_id"),nullable=False, doc='文章ID')
    parent_id = db.Column(db.Integer, db.ForeignKey("tb_article_comment.com_id"), doc='父评论id')

    like_count = db.Column(db.Integer, default=0, doc='点赞数')
    reply_count = db.Column(db.Integer, default=0, doc='回复数')
    content = db.Column(db.String(200), nullable=False, doc='评论内容')
    ctime = db.Column(db.DateTime, default=datetime.now, doc='创建时间')
    is_top = db.Column(db.Boolean, default=False, doc='是否置顶')
    status = db.Column(db.Integer, default=1, doc='评论状态')
    check_id = db.Column(db.Integer, db.ForeignKey('tb_user_basic.id'), doc='审核人员ID')
    check_time = db.Column(db.DateTime, doc='审核时间')
    delete_time = db.Column(db.DateTime, doc='删除时间')
    user = db.relationship("User", backref="comments")







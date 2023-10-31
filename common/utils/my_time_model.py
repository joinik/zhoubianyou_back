from datetime import datetime

from app import db

class TimeBaseModel:
    """模型基类，为模型补充创建时间与更新时间"""

    ctime = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 记录的创建时间
    utime = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间




# -*- coding: utf-8 -*-
# author: JK time:2021/12/26

from app import db



class Area(db.Model):
    """地区"""

    __tablename__ = 'tb_area'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, doc='地区id')
    area_name = db.Column(db.String(20), doc='地区名称')
    city_code = db.Column(db.String(12), nullable=True, doc='地区编码')
    city_level = db.Column(db.Integer, nullable=True, doc='地区级别')
    parent_id = db.Column(db.Integer, db.ForeignKey("tb_area.id"), nullable=True, doc='上级行政区')

    parent = db.relationship("Area", backref=db.backref("subs", lazy='dynamic'), remote_side=[id])

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.area_name,
            'parent': self.parent.area_name if self.parent else None,
            'city_level': self.city_level
        }




from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import db
from app.models.article import Article, Classes
from app.models.user import RoleGroup
from common.utils.decorators import login_required, permission_requeired


class ArticleManageResource(Resource):
    """管理文章类"""
    method_decorators = [login_required, permission_requeired(RoleGroup.ZMSPermission.POSTER)]
    def get(self):
        """查询各个地区的文章"""
        # 构造请求参数
        parser = RequestParser()
        parser.add_argument('area_id', location='args', type=int)    # 地区id
        parser.add_argument('classes_id', location='args', type=int) # 分类id
        parser.add_argument('page', location='args', default=1, type=int) # 查询第几页数据
        parser.add_argument('limit', location='args', default=10, type=int) # 每页查询几条


        # 获取参数
        args = parser.parse_args()
        area_id = args.area_id
        classes_id = args.classes_id
        page = args.page
        limit = args.limit

        # 查询数据库
        if classes_id:
            if area_id:
                try:
                    paginate = Article.query.options(load_only(Article.art_id)).\
                        filter(Article.classes_id == classes_id, Article.area_id == area_id).\
                        paginate(page=page, per_page=limit, error_out=False)

                except Exception as e:
                    print('根据分类id 地区id 查询文章失败')
                    print(e)
                    return {"message": "根据分类id 地区id 查询文章失败"}, 400
            else:
                try:
                    paginate = Article.query.options(load_only(Article.art_id)). \
                        filter(Article.classes_id == classes_id). \
                        paginate(page=page, per_page=limit, error_out=False)

                except Exception as e:
                    print('根据分类id 查询文章失败')
                    print(e)
                    return {"message": "根据分类id 查询文章失败"}, 400
        else:
            if area_id:
                try:
                    paginate = Article.query.options(load_only(Article.art_id)). \
                        filter(Article.area_id == area_id, Article.classes_id != 4). \
                        paginate(page=page, per_page=limit, error_out=False)

                except Exception as e:
                    print('根据地区id 查询文章失败')
                    print(e)
                    return {"message": "根据地区id 查询文章失败"}, 400
            else:
                try:
                    paginate = Article.query.options(load_only(Article.art_id)). \
                        filter(Article.classes_id != 4). \
                        paginate(page=page, per_page=limit, error_out=False)

                except Exception as e:
                    print('查询文章失败')
                    print(e)
                    return {"message": "查询文章失败"}, 400


        return {"totalPage": paginate.pages, "artList": [item.to_dict() for item in paginate.items]}


    def put(self):
        """修改文章状态"""
        parser = RequestParser()
        parser.add_argument('art_id', location='json', required=True, type=int)
        parser.add_argument('status', location='json', required=True,type=int)
        parser.add_argument('reason', location='json', required=True,type=str)
        args = parser.parse_args()
        art_id = args.art_id
        status = args.status
        reason = args.reason
        user_id = g.user_id

        try:
            # 根据id 查询数据
            rest = Article.query.options(load_only(Article.art_id)).filter(Article.art_id == art_id).\
                update({"status": status, "reason": reason, "check_id": user_id})

            db.session.commit()
            if rest:
                return {"message": "文章状态修改成功", "data": {"art_id": art_id, "status": status}}, 201

        except Exception as e:
            print('数据库修改失败')
            print(e)
            return {"message": "文章状态修改 失败，请稍后重试"}, 400






class ClassesResource(Resource):
    """文章分类管理"""
    method_decorators = [login_required, permission_requeired(RoleGroup.ZMSPermission.BOARDER)]

    def post(self):
        """创建分类"""
        parser = RequestParser()
        parser.add_argument('cla_title', location='json', required=True, type=str)

        args = parser.parse_args()
        cla_title = args.cla_title

        # 数据库查询数据
        if Classes.query.options(load_only(Classes.id)).filter(Classes.cla_title == cla_title).first():
            return {"message": "重复分类"}, 200

        else:
            cla = Classes(cla_title=cla_title)
            db.session.add(cla)
            db.session.commit()

            return {"cla_title": cla_title, "cla_id": cla.id, "ctime": cla.ctime.isoformat()}

    def get(self):

        cla = Classes.query.options(load_only(Classes.id)).all()

        rest = [{
            "id": item.id,
            "cla_title": item.cla_title
        } for item in cla]

        return rest

    def put(self):
        """修改分类"""
        parser = RequestParser()
        parser.add_argument('cla_id', location='json', required=True, type=int)
        parser.add_argument('cla_title', location='json', required=True, type=str)

        args = parser.parse_args()
        cla_title = args.cla_title
        cla_id = args.cla_id
        try:
            cla = Classes.query.options(load_only(Classes.id)).filter(Classes.id == cla_id).update({"cla_title": cla_title})
            db.session.commit()
            return {"cla_id": cla_id, "cla_title": cla_title}

        except Exception as e:
            print("分类修改失败")
            print(e)
            return {"message": "分类修改失败"}

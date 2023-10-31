from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import db
from app.models.article import Article
from app.models.comment import Comment
from app.models.user import RoleGroup
from common.utils.decorators import login_required, permission_requeired


class CommentManageResource(Resource):
    """管理评论类"""
    method_decorators = [login_required, permission_requeired(RoleGroup.ZMSPermission.COMMENTER)]
    def get(self):
        """查询评论"""
        # 构造请求参数
        parser = RequestParser()
        parser.add_argument('art_id', location='args', type=int)    # 文章id
        parser.add_argument('page', location='args', default=1, type=int) # 查询第几页数据
        parser.add_argument('limit', location='args', default=10, type=int) # 每页查询几条


        # 获取参数
        args = parser.parse_args()
        art_id = args.art_id
        page = args.page
        limit = args.limit

        # 查询数据库
        if art_id:
            try:
                paginate = Comment.query.options(load_only(Comment.com_id)).\
                    filter(Comment.article_id == art_id).\
                    paginate(page=page, per_page=limit, error_out=False)

                return {"totalPage": paginate.pages, "commentList": [item.to_dict() for item in paginate.items]}

            except Exception as e:
                print('文章id 查询评论失败')
                print(e)
                return {"message": "文章id 查询评论失败"}, 400

        else:

            try:
                paginate = Comment.query.options(load_only(Comment.com_id)). \
                    paginate(page=page, per_page=limit, error_out=False)

                return {"totalPage": paginate.pages, "commentList": [item.to_dict() for item in paginate.items]}

            except Exception as e:
                print('查询评论失败')
                print(e)
                return {"message": "查询评论失败"}, 400


    def put(self):
        """修改评论状态"""
        parser = RequestParser()
        parser.add_argument('com_id', location='json', required=True, type=int)
        parser.add_argument('status', location='json', required=True,type=int)
        args = parser.parse_args()
        com_id = args.com_id
        status = args.status
        user_id = g.user_id

        try:
            # 根据id 查询数据
            rest = Comment.query.options(load_only(Comment.com_id)).filter(Comment.com_id == com_id).\
                update({"status": status, "check_id": user_id})

            db.session.commit()
            if rest:
                return {"message": "文章状态修改成功", "data": {"com_id": com_id, "status": status}}, 201

        except Exception as e:
            print('数据库修改失败')
            print(e)
            return {"message": "文章状态修改 失败，请稍后重试"}, 400
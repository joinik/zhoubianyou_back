from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy import desc
from sqlalchemy.orm import load_only

from app import db
from app.models.article import Article, ArticleContent
from app.models.user import RoleGroup
from common.utils.decorators import login_required, permission_requeired
from common.utils.img_storage import upload_file
from common.utils.my_parser import image_file


class AnnounceResource(Resource):
    """公告类"""

    method_decorators = [login_required, permission_requeired(RoleGroup.ZMSPermission.POSTER)]

    def post(self):
        """创建公告"""
        parser = RequestParser()
        parser.add_argument('an_title', location='form', type=str)     # 公告标题
        parser.add_argument('an_content', location='form', type=str)    # 公告内容
        parser.add_argument('area', required=True, location='form', type=int)    # 公告内容

        parser.add_argument('cover', type=image_file, location='files', action='append')

        # 获取参数
        args = parser.parse_args()
        an_title = args.an_title
        an_content = args.an_content

        area = args.area
        cover = args.cover
        user_id = g.user_id

        # 公告图片字典
        cover_dict = {}
        if cover:  # 判断 特色 简介图片是否存在
            # key的值
            index_num = 0

            for img_file in cover:
                # 读取二进制数据
                img_bytes = img_file.read()
                index_num += 1
                try:
                    file_url = upload_file(img_bytes)
                    # 添加到 图片字典中
                    cover_dict[str(index_num)] = file_url
                except BaseException as e:
                    return {'message': 'thired Error: %s' % e, 'data': None}, 400

        # 公告 classes_id= 4
        # 存入数据库
        art = Article(classes_id=4, user_id=user_id, area_id=area, art_title=an_title, cover=cover_dict)

        try:
            # 提交
            print('存储公告基本信息')
            db.session.add(art)
            # 先执行插入插入操作， 才能获取article 的id
            db.session.flush()

            # 存储公告内容
            art_content = ArticleContent(article_id=art.art_id, content=an_content)
            db.session.add(art_content)
            db.session.commit()


        except Exception as e:
            print('公告，数据库，创建失败')
            print(e)
            db.session.rollback()
            return {"message": '创建失败！', "data": None}, 400

        # 序列化 数据
        rest = {
            'area_id': art.area.id,
            'area_name': art.area.area_name,
            'art_id': art.art_id,
            'title': art.art_title,
            "cover": art.cover if art.cover else None,
            'pubdate': art.ctime.isoformat(),
            'update': art.utime.isoformat(),
            'aut_id': art.user.id,
            'aut_name': art.user.nick_name,
            'content': art.article_content.content,
        }

        return rest

    def get(self):
        """查询所有的地区公告"""

        parser = RequestParser()
        parser.add_argument('area_id', location='args', type=int)
        parser.add_argument('page', default=1, location='args', type=int)
        parser.add_argument('limit', default=10, location='args', type=int)

        # 获取参数
        args = parser.parse_args()
        area_id = args.area_id
        page = args.page
        limit = args.limit

        try:
            # 地区id 存在， 则放回该地区的公告
            if area_id:
                print('地区公告查询')
                # 数据库查询
                paginate = Article.query.options(load_only(Article.art_id)). \
                    filter(Article.classes_id == 4, Article.area_id == area_id). \
                    order_by(-Article.utime).paginate(page=page, per_page=limit, error_out=False)

            # 没有的 则是返回全部的
            else:
                # 数据库查询
                paginate = Article.query.options(load_only(Article.art_id)).filter(Article.classes_id == 4). \
                   paginate(page=page, per_page=limit, error_out=False)

        except Exception as e:
            print('特色 数据库查询失败')
            print(e)
            return {"message": '查询失败！', 'data': None}, 200

        rest = [{
            'area_id': item.area.id,
            'area_name': item.area.area_name,
            'art_id': item.art_id,
            'title': item.art_title,
            "cover": item.cover,
            'pubdate': item.ctime.isoformat(),
            'update': item.utime.isoformat(),
            'aut_id': item.user.id,
            'aut_name': item.user.nick_name,
            'content': item.article_content.content,
        } for item in paginate.items]


        return {"totalPage": paginate.pages, "AnnounceList": rest}

    def put(self):
        """修改公告"""

        # 构造请求参数
        parser = RequestParser()
        parser.add_argument('announce_id', required=True, location='form', type=int)
        parser.add_argument('an_title', location='form', type=str)  # 公告标题
        parser.add_argument('an_content', location='form', type=str)  # 公告内容
        parser.add_argument('cover', type=image_file, location='files', action='append')

        # 获取参数
        args = parser.parse_args()
        an_id = args.announce_id  # 公告id
        an_title = args.an_title  # 公告标题
        an_content = args.an_content # 公告内容
        cover = args.cover           # 公告图片


        # 公告图片字典
        cover_dict = {}
        if cover:  # 判断 特色 简介图片是否存在
            # key的值
            index_num = 0

            for img_file in cover:
                # 读取二进制数据
                img_bytes = img_file.read()
                index_num += 1
                try:
                    file_url = upload_file(img_bytes)
                    # 添加到 图片字典中
                    cover_dict[str(index_num)] = file_url
                except BaseException as e:
                    return {'message': 'thired Error: %s' % e, 'data': None}, 400


        try:
            # 数据库查询
            if cover_dict != {}:
                rest = Article.query.options(load_only(Article.art_id)).filter(Article.art_id == an_id). \
                    first()
                rest.art_title = an_title
                rest.cover = cover_dict
                rest.article_content.content = an_content



            else:
                rest = Article.query.options(load_only(Article.art_id)).filter(Article.art_id == an_id). \
                    first()
                rest.art_title = an_title
                rest.article_content.content = an_content
            db.session.commit()
            if rest:
                return {"message": "公告修改成功", "data": {"announce_id": an_id}}, 201

        except Exception as e:
            print('数据库公告修改失败')
            print(e)
            return {"message": "公告修改 失败，请稍后重试"}, 200




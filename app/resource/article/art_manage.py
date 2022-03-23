from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import db
from app.models.article import Special
from app.models.user import RoleGroup
from common.utils.decorators import login_required, permission_requeired
from common.utils.img_storage import upload_file
from common.utils.my_parser import image_file


class SpecialArticleResource(Resource):
    """特色类"""
    method_decorators = [login_required, permission_requeired(RoleGroup.ZMSPermission.ANNOUNCE)]


    def post(self):
        """创建特色文章"""
        parser = RequestParser()
        parser.add_argument('desc', location='form', type=str)
        parser.add_argument('culture', location='form', type=str)
        parser.add_argument('scenery', location='form', type=str)
        parser.add_argument('snack', location='form', type=str)
        parser.add_argument('area', required=True, location='form', type=str)
        parser.add_argument('desc_photo', type=image_file, location='files', action='append')
        parser.add_argument('culture_photo', type=image_file, location='files', action='append')
        parser.add_argument('scenery_photo', type=image_file, location='files', action='append')
        parser.add_argument('snack_photo', type=image_file, location='files', action='append')

        # 获取参数
        args = parser.parse_args()
        desc = args.desc
        culture = args.culture
        scenery = args.scenery
        snack = args.snack
        area = args.area
        desc_photo = args.desc_photo
        culture_photo = args.culture_photo
        scenery_photo = args.scenery_photo
        snack_photo = args.snack_photo
        user_id = g.user_id


        # 地区简介图片字典
        desc_dict = {}
        if desc_photo:  # 判断 特色 简介图片是否存在
            # key的值
            index_num = 0

            for img_file in desc_photo:
                # 读取二进制数据
                img_bytes = img_file.read()
                index_num += 1
                try:
                    file_url = upload_file(img_bytes)
                    # 添加到 图片字典中
                    desc_dict[str(index_num)] = file_url
                except BaseException as e:
                    return {'message': 'thired Error: %s' % e, 'data': None}, 400

        # 地区文化图片字典
        cult_dict = {}
        if culture_photo:  # 判断 特色 文化图片是否存在
            # key的值
            index_num = 0

            for img_file in culture_photo:
                # 读取二进制数据
                img_bytes = img_file.read()
                index_num += 1
                try:
                    file_url = upload_file(img_bytes)
                    # 添加到 图片字典中
                    cult_dict[str(index_num)] = file_url
                except BaseException as e:
                    return {'message': 'thired Error: %s' % e, 'data': None}, 400

        # 地区美景图片字典
        scenery_dict = {}
        if scenery_photo:  # 判断 特色 美景图片是否存在
            # key的值
            index_num = 0

            for img_file in scenery_photo:
                # 读取二进制数据
                img_bytes = img_file.read()
                index_num += 1
                try:
                    file_url = upload_file(img_bytes)
                    # 添加到 图片字典中
                    scenery_dict[str(index_num)] = file_url
                except BaseException as e:
                    return {'message': 'thired Error: %s' % e, 'data': None}, 400

        # 地区小吃图片字典
        snack_dict = {}
        if snack_photo:  # 判断 特色 小吃图片是否存在
            # key的值
            index_num = 0

            for img_file in snack_photo:
                # 读取二进制数据
                img_bytes = img_file.read()
                index_num += 1
                try:
                    file_url = upload_file(img_bytes)
                    # 添加到 图片字典中
                    snack_dict[str(index_num)] = file_url
                except BaseException as e:
                    return {'message': 'thired Error: %s' % e, 'data': None}, 400

        # 进行数据存储
        # 查询 数据库中是否存有数据
        # 一个地区 只有一条特色数据
        spe = Special.query.options(load_only(Special.id)). \
            filter(Special.area_id == area, Special.user_id == user_id).first()

        if spe:
            spe.spe_desc = desc
            spe.spe_culture = culture
            spe.spe_scenery = scenery
            spe.spe_snack = snack
            spe.desc_photo = desc_dict
            spe.culture_photo = cult_dict
            spe.scenery_photo = scenery_dict
            spe.snack_photo = snack_dict

        else:
            # 存入数据库
            spe = Special(area_id=area, spe_desc=desc, spe_culture=culture,
                          spe_scenery=scenery,
                          spe_snack=snack, desc_photo=desc_dict, culture_photo=cult_dict, user_id=user_id,
                          scenery_photo=scenery_dict, snack_photo=snack_dict)

        try:
            # 提交
            db.session.add(spe)
            db.session.commit()
        except Exception as e:
            print('特色，数据库，创建失败')
            print(e)
            db.session.rollback()
            return {"message": '创建失败！', "data": None}, 400

        return {"message": "OK", "data": spe.to_dict()}


    def get(self):
        """查询所有的地区特色，包括用户的"""

        parser = RequestParser()
        parser.add_argument('type', location='args', type=str)
        parser.add_argument('page', default=1, location='args', type=int)
        parser.add_argument('limit', default=10, location='args', type=int)


        # 获取参数
        args = parser.parse_args()
        flag = args.type
        page = args.page
        limit = args.limit

        try:

            if flag == 'user':
                print('用户特色')
                # 数据库查询
                paginate = Special.query.options(load_only(Special.id)).\
                    filter(Special.spe_title.isnot(None), Special.spe_title != '').\
                    order_by(-Special.utime).paginate(page=page, per_page=limit, error_out=False)

            else:
                # 数据库查询
                paginate = Special.query.options(load_only(Special.id)).filter().\
                    order_by(-Special.utime).paginate(page=page, per_page=limit, error_out=False)

        except Exception as e:
            print('特色 数据库查询失败')
            print(e)
            return {"message": '查询失败！', 'data': None}, 200



        # rest = {
        #     "totalPage": paginate.pages, # 总页数
        #     "speList": [ item.to_dict() for item in paginate.items]
        # }
        # 此次查询数据的 最后一条的id

        return {"totalPage": paginate.pages, "speList": [ item.to_dict() for item in paginate.items]}



    def put(self):
        """修改用户的特色状态"""

        # 构造请求参数
        parser = RequestParser()
        parser.add_argument('status', location='json', type=int)
        parser.add_argument('reason', location='json', type=str)
        parser.add_argument('spe_id', location='json', type=int)

        # 获取参数
        args = parser.parse_args()
        spe_id = args.spe_id   # 特色id
        status = args.status    # 特色状态
        reason = args.reason    # 特色处理原因


        try:
            # 数据库查询
            rest = Special.query.options(load_only(Special.id)).filter(Special.id == spe_id).\
                update({"status": status, "reason": reason})

            db.session.commit()
            if rest:
                return {"message": "特色状态修改成功", "data": {"spe_id": spe_id, "status": status}}, 201
        except Exception as e:
            print('数据库修改失败')
            print(e)
            return {"message": "特色状态修改 失败，请稍后重试"}, 200

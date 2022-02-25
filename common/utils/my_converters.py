# common/utils/converters.py

from werkzeug.routing import BaseConverter


# class RegexConverter(BaseConverter):
#     def __init__(self, url_map, *args):
#         super(RegexConverter, self).__init__(url_map)
#         # 将接收到的第一个参数当做匹配规则进行保存
#         self.regex = args[0]


class MobileConverter(BaseConverter):
    """
    手机号格式
    """
    regex = r'1[3-9]\d{9}'


class UsernameConverter(BaseConverter):
    regex = r'[a-zA-Z0-9_-]{5,20}'


def register_converters(app):
    """
    向Flask app中添加转换器

    :param app: Flask app对象
    """
    app.url_map.converters['mob'] = MobileConverter
    app.url_map.converters['uname'] = UsernameConverter
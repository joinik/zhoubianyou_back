# -*- coding: utf-8 -*-
# author: JK time:2021/12/27


# common/utils/parser.py


import re
import base64
import imghdr
from datetime import datetime


def email_type(email_str):
    """
    检验邮箱格式
    :param email_str: str 被检验字符串
    :return: email_str
    """
    if re.match(r'^([A-Za-z0-9_\-\.\u4e00-\u9fa5])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$', email_str):
        return email_str
    else:
        raise ValueError('{} is not a valid email'.format(email_str))


def mobile_type(mobile_str):
    """
    检验手机号格式
    :param mobile_str: str 被检验字符串
    :return: mobile_str
    """
    if re.match(r'^1[3-9]\d{9}$', mobile_str):
        return mobile_str
    else:
        raise ValueError('{} is not a valid mobile'.format(mobile_str))

def username_type(username_str):
    """
    检验用户名格式
    :param username_str: str 被检验字符串
    :return: username_str
    """
    if re.match(r'^[a-zA-Z0-9_-]{5,20}$', username_str):
        return username_str
    else:
        raise ValueError('{} is not a valid username'.format(username_str))


def pwd_type(pwd_str):
    """
    检验密码格式
    :param pwd_str: str 被检验字符串
    :return: pwd_str
    """
    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$', pwd_str):
        return pwd_str
    else:
        raise ValueError('{} is not a valid password'.format(pwd_str))






def id_number(value):
    """检查是否为身份证号"""
    id_number_pattern = r'(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$)'
    if re.match(id_number_pattern, value):
        return value.upper()
    else:
        raise ValueError('Invalid id number.')


def action_parser(value):
    """检查是do 还是 no"""
    if re.match(r'do|no|all', value):
        return value.lower()
    else:
        raise ValueError('Invalid action')


def image_file(value):
    """
    检查是否是图片文件
    :param value:
    :return:
    """
    try:
        file_type = imghdr.what(value)
    except Exception:
        raise ValueError('Invalid image.')
    else:
        if file_type:
            return value
        else:
            raise ValueError('Invalid image.')
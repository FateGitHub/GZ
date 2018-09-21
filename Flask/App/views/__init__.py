# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/13 9:19
@Author  : Fate
@File    : __init__.py.py 蓝本初始化
'''

from .main import main
from .user import user
from .product import product
from .files import files
from .stu import stu
from .relation import rel

# app.register_blueprint(main)

# 蓝本二维元组 ((蓝本对象,'url前缀'))
BLUEPRINT_TUPLE = (
    (main, ''),
    (user, '/user'),
    (product, '/product'),
    (files, '/files'),
    (stu, '/stu'),
    (rel, '/rel')
)


# 封装一个蓝本初始化方法
def blueprint_config(app):
    for blueprint, prefix in BLUEPRINT_TUPLE:
        app.register_blueprint(blueprint, url_prefix=prefix)

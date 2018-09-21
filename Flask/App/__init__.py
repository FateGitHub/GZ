# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/13 9:13
@Author  : Fate
@File    : __init__.py.py app 初始化文件
'''

from flask import Flask
from App.config import config
from App.extensions import extensions_config
from App.views import blueprint_config  # from App.views.__init__
from App.errors import errors_config
from App.models import *

# 封装一个app创建方法
def create_app(config_name):
    app = Flask(__name__)

    # 配置一定要在扩展之前
    # 加载配置
    # app.config['SECRET_KEY'] = '123123'

    # 通过环境名找到相应的环境配置类
    app.config.from_object(config.get(config_name))

    # 加载扩展实例
    extensions_config(app)

    # 注册蓝本
    blueprint_config(app)

    # 加载错误
    errors_config(app)

    return app

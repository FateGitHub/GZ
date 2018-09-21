# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/13 9:26
@Author  : Fate
@File    : config.py 配置文件
'''

import os

# 基本路径 项目路径
# dirname 文件夹
# abspath 绝对路径
# __file__ 当前文件
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 配置基类  -- 基本配置
class Config(object):
    # 秘钥
    SECRET_KEY = '&*Rak479825*&jdh342fa%'

    # 文件上传配置

    # 允许上传后缀
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'ico', 'gif', 'bmp']
    # 允许上传大小 单位是字节 4M
    MAX_CONTENT_LENGTH = 1024 * 1024 * 4
    # 上传路径
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'App\\static\\image')

    # 上传集上传路径 UPLOADED_上传集名_DEST
    UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'App\\static\\image')

    # 忽略警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 配置邮件
    # 服务器
    MAIL_SERVER = 'smtp.aliyun.com'
    # 用户名
    MAIL_USERNAME = 'fate9527@aliyun.com'
    # 密码
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') or 'Changeme_123'

    # 调试模式
    DEBUG = True  # 发布的时候 False
    DEBUG_TB_INTERCEPT_REDIRECTS = False


# 开发环境
class DevelopmentConfig(Config):
    # 连接数据库
    # 自带数据库 sqlite
    # 'sqlite:///' + 路径 + 数据库名
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'flask.sqlite')

    # mysql 'mysql+驱动(可以不写)://用户名:密码@主机:端口/数据库'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/flask'
    pass


# 测试环境
class TestConfig(Config):
    pass


# 数据库配置字典
DATABASE_CONFIG = {
    'database_name': 'mysql',
    'database_drive': 'pymysql',
    'username': 'root',
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': '127.0.0.1',
    'port': os.getenv('MYSQL_PORT'),
    'database': 'flask'
}


# 发布环境
class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = '{database_name}+{database_drive}:' \
                              '//{username}:{password}@{host}:{port}/{database}'.format(**DATABASE_CONFIG)


# 配置环境字典
config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'product': ProductConfig,
    'default': DevelopmentConfig
}

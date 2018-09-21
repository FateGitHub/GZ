# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/13 9:20
@Author  : Fate
@File    : extensions.py 扩展文件
'''

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_uploads import UploadSet, IMAGES
from flask_uploads import configure_uploads, patch_request_class
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

# 实例一个用户管理
login_manager = LoginManager()
# 登录端点  如果没登录 就会跳转到登陆页面
login_manager.login_view = 'user.user_login'
# 登录提示消息
login_manager.login_message = '请登录'
# session保护 默认base 可以登录多了
login_manager.session_protection = 'strong'

# 创建实例
bootstrap = Bootstrap()
moment = Moment()  # 时间

'''
name='files',  上传集名
extensions 允许上传文件
'''
IMAGE = tuple('jpg ico gif'.split())
# 实例一个上传集对象 ,默认允许上传所有
photos = UploadSet('photos', IMAGE)

# 实例一个数据对象
db = SQLAlchemy()
# 实例一个db管理对象
migrate = Migrate()

# 实例一个邮箱对象
mail = Mail()

# 调试模式
toolbar = DebugToolbarExtension()


# 封装一个扩展方法
def extensions_config(app):
    # 安装实例
    bootstrap.init_app(app)  # Bootstrap(app)

    moment.init_app(app)

    # 配置上传集
    configure_uploads(app, photos)
    # 如果size = None 那就 MAX_CONTENT_LENGTH生效
    patch_request_class(app, size=10 * 1024 * 1024)

    db.init_app(app)
    migrate.init_app(app, db)

    mail.init_app(app)

    toolbar.init_app(app)

    login_manager.init_app(app)

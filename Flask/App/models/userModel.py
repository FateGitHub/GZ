# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/14 15:32
@Author  : Fate
@File    : userModel.py 用户数据模型
'''

from flask import current_app
from flask import flash

from App.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from App.extensions import login_manager
from flask_login import UserMixin


# Timed 过期
# JSON json.dumps({})
# Web
# Signature 签名
# Serializer 序列化


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    # 用户名
    username = db.Column(db.String(32), unique=True)
    # 密码 保存到数据库里面
    password_hash = db.Column(db.String(128), nullable=False)
    # 头像 保存图片名 或图片路径
    avatar = db.Column(db.String(128), nullable=True)

    # 邮件
    mail = db.Column(db.String(64), nullable=False, unique=True)
    # 用户状态 0为激活 1 激活 2 vip 3svip
    is_active = db.Column(db.Boolean(), default=False)

    # 将方法变成属性
    # user.password
    @property
    def password(self):
        raise AttributeError('密码不可读')

    # 给保护字段赋值
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 校验密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成token
    def generate_token(self, expires=3600):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'], expires_in=expires)
        # dumps 序列化{}
        return s.dumps({'id': self.id})

    @staticmethod
    def user_active(token):
        s = Serializer(secret_key=current_app.config['SECRET_KEY'])
        # 校验token
        try:
            # 解析token
            data = s.loads(token)
        # 过期
        except SignatureExpired:
            flash('邮件已过期，请重新发送')
            return False

        # 是否被修改
        except BadSignature:
            flash('邮件损坏，请重新发送')
            return False
        # 找到用户

        user = Users.query.get(int(data.get('id')))

        if user:
            # 修改用户状态
            # 没激活，就激活
            if not user.is_active:
                user.is_active = True
                db.session.add(user)
                flash('用户已激活，请登录')
            else:
                flash('用户已激活，请登录')
        else:
            flash('用户不存在，请注册')

        return True


# login—manager登录回调
@login_manager.user_loader
def load_user(uid):
    return Users.query.get(int(uid))

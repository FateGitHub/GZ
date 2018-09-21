# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/13 9:56
@Author  : Fate
@File    : user.py 用户视图
'''
import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from App.forms import UserLogin, UserRegister
from werkzeug.security import generate_password_hash
from App.extensions import photos
from App.models import Users
from App.extensions import db
import uuid
from App.email import send_mail
from flask_login import login_user, logout_user, login_required

user = Blueprint('user', __name__)


@user.route('/login/', methods=['GET', 'POST'])
def user_login():
    form = UserLogin()

    # 提交判断
    if form.validate_on_submit():
        # 成功后重定向 到首页
        # 校验用户，不存在就注册
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if not user.is_active:
                flash('账号未激活')
            # check_password_hash() 校验密码
            if not user.check_password(form.password.data):
                flash('密码错误')
            else:
                # 正确跳转到首页
                # 使用login-manager保存用户
                login_user(user)
                # 就会生成一个current_user的全局变量
                response = redirect(url_for('main.hello_main'))
                return response
    return render_template('user/login.html', form=form)


@user.route('/loginout/')
def login_out():
    logout_user()
    return redirect(url_for('main.index'))


@user.route('/user_register/', methods=['GET', 'POST'])
def user_register():
    # 注册表单对象
    form = UserRegister()
    # 判断提交
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # 密码需要加密
        password = generate_password_hash(password)
        # 保存图片
        avatar = form.avatar.data
        avatar_name = avatar.filename
        # 图片后缀
        suffix = os.path.splitext(avatar_name)[1]
        affix = uuid.uuid4()
        avatar_name = str(affix) + suffix

        # 使用上传集保存图片
        photos.save(avatar, name=avatar_name)

        # 保存到数据库
        user = Users()
        user.username = username
        user.password = password
        user.avatar = avatar_name
        db.session.add(user)

        flash('注册成功')

    return render_template('user/register.html', form=form)


@user.route('/register/', methods=['GET', 'POST'])
def register():
    # 生成表单
    form = UserRegister()
    # 判断是否提交，数据合理性
    if form.validate_on_submit():
        # 获取表单数据
        # username = form.username.data
        user = Users(username=form.username.data,
                     password=form.password.data,
                     mail=form.email.data)

        # 保存图片
        avatar = form.avatar.data
        avatar_name = avatar.filename
        # 图片后缀
        suffix = os.path.splitext(avatar_name)[1]
        affix = uuid.uuid4()
        # 图片名
        avatar_name = str(affix) + suffix

        # 使用上传集保存图片
        photos.save(avatar, name=avatar_name)

        user.avatar = avatar_name
        # 保存
        db.session.add(user)
        # 保证数据库必须有数据
        # 提交 自动保存是 方法执行完才提交
        db.session.commit()

        # 认识是哪个用户
        # 手动构建的一个会话 token
        # 生成一个token
        token = user.generate_token()
        # 激活相对应用户
        # 发送激活邮件
        send_mail(subject='用户激活',
                  recipients=form.email.data,
                  email_tmp='active',
                  username=form.username.data,
                  token=token)
        flash('邮件已发送，请跳转激活')

    return render_template('user/register.html', form=form)


@user.route('/active/<token>/')
def active(token):
    '''
    点击激活
    :param token 会话 包含了用户信息 id
    :return:
    '''
    if Users.user_active(token):
        # 激活了就重定向到登录页面
        return redirect(url_for('user.user_login'))
    else:
        # 重新发送邮件
        return '重新发送邮件'


@user.route('/send_mail/')
def send_email():
    send_mail(subject='激活',
              recipients='fate9527@aliyun.com',
              email_tmp='active',
              username='fate')

    return '邮箱发送成功'


# 先执行里层的，
@user.route('/mybook/')
@login_required
def my_book():
    # 必须登陆
    return '我的订单'

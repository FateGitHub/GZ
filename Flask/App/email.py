# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/18 14:58
@Author  : Fate
@File    : email.py 邮箱 工具 通用性
'''

from App.extensions import mail
from flask_mail import Message
from flask import current_app, render_template
import time
import threading


# 解决 邮箱阻塞
# 异步发送
# 开辟一条新的线程 threading.Thread()


def async_send_mail(app, msg):
    # 使用新的线程发送邮件
    # 使用完了需要关闭
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipients, email_tmp, **kwargs):
    '''
    发送邮件
    :param subject 主题
    :param recipients 接收邮箱
    :param email_tmp 模板名
    :param **kwargs不定长关键字参数 {}
    :return:
    '''
    '''
    subject: 主题
    recipients: 接收邮箱 list
    body: 文本消息
    html: HTML 消息
    sender: 发送者邮箱
    cc: 抄送 list
    bcc: 密送 list
    '''
    # time.sleep(5)

    '''
    msg = Message(subject='激活邮箱',
                  # recipients=['10000@qq.com'],
                  recipients=['fate9527@aliyun.com'],
                  sender=current_app.config['MAIL_USERNAME'],
                  # cc=['1687458949@qq.com'],
                  )
    '''


    msg = Message(subject=subject,
                  recipients=[recipients],
                  sender=current_app.config['MAIL_USERNAME'],
                  )

    msg.html = render_template('email/' + email_tmp + '.html', **kwargs)
    # msg.html = '<h1>啊啊啊啊啊</h1>'
    # 发送邮件 可能阻塞
    # mail.send(msg)

    # 获取真实的APP对象
    app = current_app._get_current_object()
    # 创建一条线程
    t = threading.Thread(target=async_send_mail, args=(app, msg))
    # 启动线程
    t.start()

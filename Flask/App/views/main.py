# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/13 9:48
@Author  : Fate
@File    : main.py 主视图
'''

from flask import Blueprint, render_template, request

# 实例蓝本对象 (蓝本名,__name__)
main = Blueprint('main', __name__)


@main.route('/')
def hello_main():
    return render_template('base.html')


@main.route('/index/')
def index():
    return render_template('base.html')

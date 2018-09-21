# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/18 16:46
@Author  : Fate
@File    : errors.py 错误模块
'''
from flask import render_template


# 封装一个捕捉 错误方法
def errors_config(app):
    @app.errorhandler(404)
    def err_404(e):
        return render_template('error/404.html')

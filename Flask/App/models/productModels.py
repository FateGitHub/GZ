# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/18 9:09
@Author  : Fate
@File    : productModels.py 产品模型
'''

from App.extensions import db


# 咖啡
class Coffees(db.Model):
    # 表名
    __tablename__ = 'coffees'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    # 咖啡名
    coffee_name = db.Column(db.String(64), nullable=False)
    # 图片
    coffee_img = db.Column(db.String(128), nullable=False)

# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/13 10:06
@Author  : Fate
@File    : product.py
'''

from flask import Blueprint, render_template
from App.models import Coffees
import random
from App.extensions import db

product = Blueprint('product', __name__)


@product.route('/index/<int:id>')
def product_index(id):
    '''
    产品首页
    :param id 商品id
    :return:  产品首页信息
    '''
    return "product Index"


@product.route('/insert/')
def insert_coffee():
    # 插入100条
    coffee_name_list = ['凤舞祥云综合咖啡豆',
                        '烘焙咖啡豆', '肯亚咖啡豆']

    coffee_img_list = ['kenya-coffee-beans.png',
                       'komodo-dragon-blend-coffee-beans.png',
                       'south-of-the-clouds.jpg']

    coffee_list = []
    for i in range(100):
        # 实例coffee模型
        coffee = Coffees()
        coffee.coffee_name = random.choice(coffee_name_list) + str(i)
        coffee.coffee_img = random.choice(coffee_img_list)
        coffee_list.append(coffee)

    # 插入全部
    db.session.add_all(coffee_list)

    return 'coffee插入成功'


@product.route('/coffee/<int:page>')
def show_coffee(page=1):
    '''
    展示coffee
    :return:
    '''

    '''
    # 从数据库查询
    coffee_list = Coffees.query.all()
    for coffee in coffee_list:
        print(coffee.coffee_name)
    '''

    '''
    page=None, 当前页码 默认第一页
    per_page=None, 每页显示的个数 默认20个
    error_out=True, 超出报404错误
    max_per_page=None ,每页显示的最大个数

    items = self.limit(per_page).offset((page - 1) * per_page).all()

    '''
    coffee_list = Coffees.query.paginate(page=page, per_page=8, error_out=False)
    print(type(coffee_list))
    return render_template('product/coffee.html', coffee_list=coffee_list)

# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/14 9:47
@Author  : Fate
@File    : stu.py 学生视图
'''

from flask import Blueprint, render_template
from sqlalchemy import and_, or_, not_
from App.extensions import db
from App.models import Students
import random
import string

stu = Blueprint('stu', __name__)


@stu.route('/create/')
def create_table():
    # 生成表
    db.create_all()

    return '表创建成功'


@stu.route('/drop/')
def drop_table():
    # 删除表
    db.drop_all()
    return '表删除成功'


@stu.route('/insert/')
def insert_stu():
    '''
    # sql = ' insert into students() VALUES ()'
    # 实例一个学生对象
    stu = Students()

    stu.stu_name = '王五'
    stu.stu_num = '733425'
    stu.hobby = 'look video'

    # 添加到数据里面去
    db.session.add(stu)
    # 提交
    # db.session.commit()
    '''

    stu_list = []
    for i in range(20):
        stu = Students()
        stu.stu_name = '学生%d' % i
        # string.digits 0-9数字
        # for _ in range() 只做循环
        stu.stu_num = ''.join(random.choice(string.digits) for _ in range(5))
        stu.stu_age = random.randint(3, 40)
        stu.hobby = random.choice(['play game', 'watch av', 'click code'])

        stu_list.append(stu)

    # 添加多个 .add_all()
    # 添加一个.add()
    db.session.add_all(stu_list)
    return '学生插入成功'


@stu.route('/select/')
def select_stu():
    # 数据库 小写转大写
    '''
    sql = 'SELECT * FROM students'
    stus = db.session.execute(sql)
    print(type(stus))

    for s in stus:
        print(s)

    '''

    # 对象.query.
    # .all() 所有
    stus = Students.query.all()  # 列表 [对象]
    print(stus)

    # 查询张三
    # get(id) 通过id查找
    zs = Students.query.get(3)
    #

    # 查询性别 sex = 0
    # filter = sql where
    # filter(对象.属性 == 条件) == >= <= != __gt__, __lt__, __eq__,__ge__
    # sex0 = Students.query.filter(Students.stu_sex == 0).all()

    # filter_by 等值条件查询 =
    sex0 = Students.query.filter_by(stu_sex=0).all()

    # 年龄大于20 的e
    # first() 取第一个
    # ages = Students.query.filter(Students.stu_age > 50).first()
    # first_or_404() 没有返回404
    # ages = Students.query.filter(Students.stu_age > 50).first_or_404()

    # ages = Students.query.filter(Students.stu_age.__ge__(20)).all()
    # id = 30 get 不存在返回None
    # id30 = Students.query.get(30)

    # id30 = Students.query.get_or_404(30)

    # 多条件查询
    # 年龄=18 爱看片  and filter(条件1,条件2,....)
    # stus = Students.query.filter(Students.stu_age < 18, Students.hobby == 'watch av').all()

    # stus = Students.query.filter(Students.stu_age < 18 and Students.hobby == 'watch av').all()

    # and_
    # stus = Students.query.filter(and_(Students.stu_age < 18, Students.hobby == 'watch av')).all()

    # or_ 或
    # 年龄 19 爱敲代码 或 19男生
    stus = Students.query.filter(or_(and_(Students.stu_age == 19, Students.hobby == 'click code'),
                                     and_(Students.stu_age == 19, Students.stu_sex == 1)))

    # not_ 非
    stus = Students.query.filter(not_(and_(Students.stu_age == 19)),
                                 and_(Students.stu_age == 20))

    # limit() 限制输出个数
    stus = Students.query.limit(10).all()

    # offset() 偏移量
    stus = Students.query.offset(3).limit(10).all()

    # 排序
    # 按年龄排序 最大年龄 输出前三
    # order_by(字段) 默认升序 降序 -字段名
    stus = Students.query.order_by('-stu_age').limit(3)

    # for s in stus:
    #     print(s.stu_age)

    return '学生查询成功 % s' % stus


# 更新
@stu.route('/update/<int:id>')
def update_stu(id):
    # 先查找
    stu = Students.query.get(id)

    # 改成张三
    stu.stu_name = '张三'

    # 更新
    db.session.add(stu)
    # db.session.commit()
    return '修改成功'


# 删除
@stu.route('/delete/<int:id>')
def delete_stu(id):
    # 先查找
    stu = Students.query.get(id)
    # 后删除
    db.session.delete(stu)
    return '删除成功'


# 分页
@stu.route('/paginate/<int:page>')
def paginate_stu(page=1):
    stus = Students.query.paginate(page, 4, False)
    return render_template('stu/paginate.html', stus=stus)

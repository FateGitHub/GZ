# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/18 11:09
@Author  : Fate
@File    : relation.py
'''
import random

from flask import Blueprint
from App.models import Teacher, Email, Article, Tag
from App.extensions import db

rel = Blueprint('rel', __name__)


# 插入老师
@rel.route('/insert_t/')
def insert_teacher():
    tList = []
    for i in range(20):
        u = Teacher(teacher_name="老师%d" % i)
        tList.append(u)

    db.session.add_all(tList)
    db.session.commit()
    return 'teacher 表数据插入成功'


@rel.route('/insert_e/')
def insert_address():
    emailList = []
    for i in range(30):
        e = Email(email=''.join(str(random.randint(0, 9)) for _ in range(9)) + random.choice(
            ['@qq.com', '@163.com', '@aliyun.com', '@sina.com']), t_id=random.randint(1, 20))
        emailList.append(e)

    db.session.add_all(emailList)
    db.session.commit()
    return 'Email 表数据插入成功'


# 查询老师1的所有邮箱
@rel.route('/select/')
def select():
    t0 = Teacher.query.filter_by(teacher_name='老师0').first()
    print(t0)
    # emails = Email.query.filter(Email.t_id == t0.id).all()
    # print(emails)

    print(t0.mail, '===============')

    # 通过 353345919@sina.com 找到老师

    sql = "select * from teacher as t " \
          "join email e on e.t_id=t.id " \
          "where e.email='353345919@sina.com'"

    e = Email.query.filter_by(email='353345919@sina.com').first()

    t = Teacher.query.filter(Email.query.filter_by(email='353345919@sina.com'))

    print(t)
    print(e.teacher)
    return '查询成功'


# 插入 多对多
@rel.route('/many_to_many/')
def many_to_many():
    # 文章
    article1 = Article(title='金瓶梅')
    article2 = Article(title='少年阿宾')
    article3 = Article(title='我的兄弟叫顺溜')

    # 章节
    tag1 = Tag(name='第一章第一回')
    tag2 = Tag(name='第一章第二回')
    tag3 = Tag(name='第二章第一回')

    # 建立多对多关系 多表关系插入 表1.relationship.append(表2)
    article1.tag.append(tag1)
    article1.tag.append(tag2)

    article2.tag.append(tag1)
    article2.tag.append(tag3)

    article3.tag.append(tag2)
    article3.tag.append(tag3)

    # 插入数据库
    db.session.add(article1)
    db.session.add(article2)
    db.session.add(article3)

    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)

    return '多对多插入成功'


# 查询
@rel.route('/many_select/')
def many_select():
    # 金瓶梅的所有章节
    article = Article.query.filter_by(title='金瓶梅').first()
    print(article.tag)
    for tag in article.tag:
        print(tag.name)
    return '查询成功'

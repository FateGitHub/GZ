# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/18 10:57
@Author  : Fate
@File    : relationModel.py
'''

from App.extensions import db


# 用户邮箱模型 一对多

# 老师模型
class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    teacher_name = db.Column(db.String(32))

    def __repr__(self):
        return self.teacher_name


# 邮箱
class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(64))

    # 一对多
    # 声明外键 一般放在多的一方
    # db.ForeignKey(表名.主键)
    t_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))

    # Teacher.mail << ==== >>Email.teacher 双向关系
    # 反向查询
    teacher = db.relationship('Teacher', backref='mail')

    def __repr__(self):
        return self.email


# 使用中间表关联 多对对
article_tag = db.Table(
    'article_tag',  # 表名
    db.Column('article_id', db.Integer(), db.ForeignKey('article.id'), primary_key=True),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id'), primary_key=True)
)


# 文章
class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer(), primary_key=True)
    # 书名
    title = db.Column(db.String(32), nullable=False)

    # 双向关系
    tag = db.relationship('Tag', secondary=article_tag, backref='article')


# 章节
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer(), primary_key=True)
    # 章节名
    name = db.Column(db.String(64), nullable=False)

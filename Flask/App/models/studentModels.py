# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/14 9:35
@Author  : Fate
@File    : studentModels.py 学生数据模型
'''

from App.extensions import db


class Students(db.Model):
    # 表名
    # 默认情况
    # 类名 大写变小写,第二个大写字母前面加下划线 students
    # StudentModel student_model

    __tablename__ = 'students'

    # 主键 如果设置为主键 ，就默认自动增长
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    # 学生名
    stu_name = db.Column(db.String(32), nullable=False)
    # 学号
    stu_num = db.Column(db.String(8), nullable=False)
    # 性别
    stu_sex = db.Column(db.Boolean, default=True)
    # 年龄
    stu_age = db.Column(db.SmallInteger, default=18)
    # 爱好
    hobby = db.Column(db.String(64))

    # print 输出
    # def __str__(self):
    #     return self.stu_name
    def __repr__(self):
        return self.stu_name

# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/13 9:10
@Author  : Fate
@File    : manage.py 管理文件
'''
# from flask import Flask
from flask_script import Manager, prompt_bool
from App import create_app
import os
from App.extensions import db
from flask_migrate import MigrateCommand

# 指定环境
# win set CONFIG_NAME=development  查看 set CONFIG_NAME
# linux export CONFIG_NAME=development 查看echo $CONFIG_NAME

config_name = os.getenv('CONFIG_NAME') or 'default'
app = create_app(config_name)

# app = Flask(__name__)
manager = Manager(app)

# 添加manager 命令 ( 命令名, 命令参数)
manager.add_command('db', MigrateCommand)


# python manage.py db init 创建迁移文件夹
# python manage.py db migrate 生成迁移文件
# python manage.py db upgrade 生成表


# @app.route('/')
# def hello():
#     return "OK"

# manager添加命令
@manager.command
def create():
    # 创建好了，不能添加新字段
    db.create_all()
    return '表创建成功'


@manager.command
def drop():
    if prompt_bool('是否删除表'):
        db.drop_all()
        return '删数据库跑路'
    else:
        return '谢谢放过'

'''
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@app.route('/ser/')
def serializer():
    s = Serializer(secret_key='8aisdf234')
    return s.dumps({'id': 1})

@app.route('/loadsSer/')
def loads_ser():
    s = Serializer(secret_key='8aisdf234')
    data = s.loads('eyJhbGciOiJIUzI1NiIsImlhdCI6MTUzNzMyMzgwMiwiZXhwIjoxNTM3MzI3NDAyfQ.eyJpZCI6MX0._NXUK8PbbS45_rXLDRiVj6L6HJxjz58EDwq2yGSED8k')
    return '%s' % data
'''
if __name__ == '__main__':
	'''
	改了bug
	'''
    manager.run()

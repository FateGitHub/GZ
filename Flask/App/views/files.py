# -*- coding:utf-8 -*-
'''
@Time    : 2018/9/13 14:28
@Author  : Fate
@File    : files.py 文件上传
'''

from flask import Blueprint, render_template, request, flash, current_app
from flask import url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
from PIL import Image  # 图片处理
from App.extensions import photos  # 导入上传集对象

files = Blueprint('files', __name__)


def allowed_extension(filename):
    '''
    判断文件后缀
    :param filename: 文件名
    :return: True or False
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


@files.route('/original_file_upload/', methods=['GET', 'POST'])
def original_file_upload():
    '''
    原生文件上传
    :return:
    '''

    img_url = None
    # 获取上传对象
    if request.method == 'POST':
        file = request.files.get('photo')
        if file:

            # 判断文件名是否安全
            # 获取文件名
            filename = file.filename
            # 不允许中文
            # filename = secure_filename(filename)

            print(filename, '==========')

            print(file, type(file))
            # 判断文件是否符合上传规定

            # 获取到配置
            # 后缀
            # current_app.config['ALLOWED_EXTENSIONS']
            if allowed_extension(filename):
                # 保存
                # 修改文件名
                # 随机生成一文件名

                # 文件后缀
                suffix = os.path.splitext(filename)[1]
                # 随机文件名
                affix = uuid.uuid4()
                # 合成
                filename = str(affix) + suffix

                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                # 打开图片
                img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                img = Image.open(img_path)
                # 修改图片尺寸
                img.thumbnail((128, 128))
                # 保存
                img.save(img_path)

                flash('文件上传成功')

                # 显示图片
                img_url = url_for('files.show_img', filename=filename)

            else:
                flash('文件格式不正确')

        else:
            flash('请选择上传文件')

    return render_template('file/original_upload.html', img_url=img_url)


@files.route('/show_img/<filename>')
def show_img(filename):
    '''
    展示图片
    :param filename 文件名
    :return: 图片路径
    '''
    '''
    directory, 目录
    filename 文件名
    '''
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@files.route('/upload/', methods=['GET', 'POST'])
def uploads_set():
    '''
    使用上传集上传
    :return:
    '''
    # 获取上传对象
    img_url = None
    if request.method == 'POST':
        file = request.files.get('photo')
        # 修改文件名
        filename = file.filename

        # 文件后缀
        suffix = os.path.splitext(filename)[1]
        # 随机文件名
        affix = uuid.uuid4()
        # 合成
        filename = str(affix) + suffix
        # 使用上传集对象保存
        '''
        storage, 文件对象
        folder=None, 文件夹
        name=None 文件名
        '''
        photos.save(file, name=filename)

        # 获取图片路径
        img_url = photos.url(filename)

    return render_template('file/original_upload.html', img_url=img_url)

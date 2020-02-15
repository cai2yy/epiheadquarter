from flask import render_template, flash, redirect, url_for, Blueprint

user_bp = Blueprint('user', __name__)


@user_bp.route('/upload', methods=['POST'])
def upload_training_set():
    # 公司用户权限
    # 接受训练集文件并上传
    # 等待训练结束更改用户当前状态
    return 1


@user_bp.route('/trainingset')
def get_training_set_status():
    # 公司用户权限
    # 查看该用户的训练集训练状态
    return 1


@user_bp.route('/results')
def get_training_results():
    # 公司用户权限
    # 查看该用户的文章训练结果
    return 1


@user_bp.route('/results/download/<int:result_id>')
def download_result(result_id):
    # 公司用户权限
    # 下载文章训练结果
    return 1


@user_bp.route('/collection')
def get_collection():
    # 普通用户权限
    # 查看用户收藏文章
    return 1


@user_bp.route('/crawler/close')
def close_crawler():
    # 管理员权限
    # 停止抓取文章
    return 1


@user_bp.route('/crawler/open')
def open_crawler():
    # 管理员权限
    # 继续抓取文章
    return 1


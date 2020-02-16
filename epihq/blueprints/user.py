from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user
from epihq.models import User, Article, Comment, Role
from epihq.extensions import db
from epihq.forms import CommentForm
from epihq.utils import redirect_back

user_bp = Blueprint('user', __name__)

"""
账户模块
@author: 
@time: 
"""


@user_bp.route('/account')
def my_account():
    # todo 账户详情页
    return render_template('user/account.html')


@user_bp.route('/account/edit')
def edit_account():
    # todo 编辑账户信息
    return render_template('user/edit.html')


@user_bp.route('/account/edit/save')
def save_account():
    # todo 编辑账户，提交表单信息到数据库
    return redirect(url_for('.my_account'))


"""
收藏模块
@author: 
@time: 
"""


@user_bp.route('/marks')
def my_marks():
    return render_template('user/marks.html')


"""
nlp模块
@author: 
@time: 
"""


@user_bp.route('/nlp', methods=['GET'])
def show_nlp():
    flash("请先登录")
    return redirect('/hello')


@user_bp.route('/nlp', methods=['POST'])
def post_nlp():
    return "post_nlp"


@user_bp.route('/trainings')
def my_training_set():
    return render_template('user/trainings.html')


@user_bp.route('/trainings/upload')
def upload_training_set():
    # FTP操作
    return 'fuck sky'


"""
训练任务模块
@author: 
@time: 
"""


@user_bp.route('/tasks')
def my_tasks():
    return render_template('user/tasks.html')


@user_bp.route('/tasks/run/<int:task_id>')
def training_run(task_id):
    return redirect_back()


@user_bp.route('/tasks/stop/<int:task_id>')
def training_stop(task_id):
    return redirect_back()


@user_bp.route('/tasks/delete/<int:task_id>')
def training_delete(task_id):
    return redirect_back()


@user_bp.route('/tasks/result/<int:task_id>')
# 应当满足一定条件：任务训练结束后出现
def training_result(task_id):
    return render_template('user/result.html')

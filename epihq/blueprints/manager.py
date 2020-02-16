from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user
from epihq.models import User, Article, Comment, Role, Mark
from epihq.extensions import db
from epihq.forms import CommentForm
from epihq.utils import redirect_back
from json import dumps

manager_bp = Blueprint('manager', __name__)


"""
------------------留待第二次迭代------------------
"""


@manager_bp.route('/manager')
def home_article():
    return render_template('manager/home.html')


"""
------------------以下为测试模块 -------------------------
"""


@manager_bp.route('/hello', methods=['GET'])
def hello():
    return redirect_back()


@manager_bp.route('/hello/<string:word>', methods=['POST'])
def hello_swagger2(word):
    """
            Test
            ---
            tags:
              - Test Swagger API
            parameters:
              - name: word
                in: path
                type: string
                required: true
            responses:
              500:
                description: 错误！
              200:
                schema:
                  id: 结果
                  properties:
                    sentence:
                      type: string
                      default: "yes!"
            """
    return "Hello,swagger" + word


@manager_bp.route('/example')
def example():
    if db.session:
        # 跳转到上一个页面
        return redirect_back()
    if db:
        # 跳转到url: /account/edit
        return redirect('/account/edit')
    if User:
        # 跳转到news蓝图下的home_article方法
        return redirect(url_for('news.home_article'))
    article = "fake_article"
    # 在当前url(/marks)，用括号里这个html文件渲染，后面紧跟的是传入前端页面的参数
    return render_template('user/marks.html', article=article)


@manager_bp.route('/sqltest')
def sql_test():
    user1 = User(username='user1', password='22', name='cai2yy', email='ss@nju.com', phone='12222222055', role_id=1)
    db.session.add(user1)
    db.session.commit()
    user = User.query.filter_by().first()
    return user.user_name + " : " + user.name


@manager_bp.route('/create')
def create():
    db.create_all()
    return "创建成功"
from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from epihq.utils import redirect_back
from epihq.forms import LoginForm
from epihq.extensions import db
from epihq.models import User

auth_bp = Blueprint('auth', __name__)


"""
注册&登录模块
@author: 
@time: 
"""


@auth_bp.route('/sign')
def sign_in():
    # todo 注册
    return render_template('auth/sign.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = User.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back.', 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    # flask_login自带函数
    logout_user()
    # 弹窗
    flash('Logout success.', 'info')
    # 回到默认页
    return redirect_back()


"""
------------------以下为测试模块 -------------------------
"""


@auth_bp.route('/example')
def example():
    if LoginForm:
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


@auth_bp.route('/hello')
def hello():
    return "hello,world!"


@auth_bp.route('/sqltest')
def sql_test():
    user1 = User(user_name='user1', password='22', name='cai2yy', email='ss@nju.com', phone='12222222055', role_id=1)
    db.session.add(user1)
    db.session.commit()
    user = User.query.filter_by().first()
    return user.user_name + " : " + user.name


import random
from flask import render_template, flash, redirect, url_for, Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from epihq.utils import redirect_back
from epihq.forms import LoginForm
from epihq.extensions import db, Swagger, swag_from
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



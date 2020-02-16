import random
from flask import render_template, flash, redirect, url_for, Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from epihq.utils import redirect_back
from epihq.forms import LoginForm, SettingForm, SignIn
from epihq.extensions import db, Swagger, swag_from
from epihq.models import User, Role

auth_bp = Blueprint('auth', __name__)

"""
注册&登录模块
@author: 
@time: 
"""


@auth_bp.route('/signIn', methods=['GET', 'POST'])
def sign_in():
    form = SignIn()
    print(form)
    print(request.method)
    if request.method == 'POST':
        print('**************************')
        username = request.form.get('username')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')
        user_name = request.form.get('user_name')
        user_phone = request.form.get('user_phone')
        user_email = request.form.get('user_email')
        roleLevel = form.roleLevel.data
        print(username)
        if form.validate_on_submit():
            new_user = User(username=username, password=password, name=user_name, phone=user_phone, email=user_email,
                            role_id=db.session.query(Role).filter_by(name=roleLevel).first().id)
            db.session.add(new_user)
            db.session.commit()
            flash('恭喜你这个混蛋，注册成功')
            return render_template('login.html', form=LoginForm())
        else:
            flash('参数有误请重新输入')
    return render_template('auth/sign.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = db.session.query(User).filter_by(username=username).first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcome back.', 'info')
                return render_template('index.html')
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

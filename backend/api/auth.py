from flask import render_template, flash, redirect, Blueprint, request, make_response, jsonify, url_for, abort
from json import dumps
from flask_login import login_user, logout_user, current_user
from backend.utils.helper import redirect_back
from backend.forms import LoginForm
from backend.utils.extensions import db, swag_from
from backend.models import User
from backend.utils.const import JSON

auth_bp = Blueprint('auth', __name__)

"""
注册&登录模块
@author: Cai2yy
@time: 20/2/18
"""


@auth_bp.route('/register', methods=['POST'])
@swag_from('../apidocs/register.yml')
def register():
    data = request.form.to_dict()
    print(data)
    if not data:
        return make_response(500)
    user = User(username=data['username'], password=data['password'], name=data['name'],
                email=data['email'], phone=data['phone'], role_id=data['role_id'])
    db.session.add(user)
    db.session.commit()
    resp = make_response(jsonify(data), 201)
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    resp.headers['Location'] = 'users/' + str(user.id)
    return resp


@auth_bp.route('/login', methods=['POST'])
@swag_from('../apidocs/login.yml')
def login():
    if current_user.is_authenticated:
        return redirect_back()
    data = request.form
    if not data:
        return make_response(500)
    user = db.session.query(User).filter_by(username=data['username']).first()
    if user:
        if user.validate_password(data['password']):
            login_user(user, data['remember'])
            flash('登陆成功.', 'info')
            print('登陆成功')
            return make_response(205)
        flash('密码错误', 'warning')
        print('密码错误')
        return make_response(403)
    flash('用户名不存在', 'warning')
    print('用户名不存在')
    return make_response(403)


@auth_bp.route('/logout')
def logout():
    """
    退出登录
    ---
    tags:
        - 用户
    responses:
        '205':
            description: 退出登录成功
    """
    logout_user()
    flash('已退出登录', 'info')
    print('退出登录')
    return make_response(205)

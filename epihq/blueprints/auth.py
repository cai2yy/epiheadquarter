from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user
from epihq.models import User, Article, Comment, Role
from epihq.extensions import db
from epihq.forms import CommentForm
from epihq.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 用户权限判断
    return 1


@auth_bp.route('/logout')
def logout():
    return 1


# 测试API
@auth_bp.route('/hello')
def hello():
    return "hello,world!"


# 测试API
@auth_bp.route('/sqltest')
def sql_test():
    user1 = User(user_name='user1', password='22', name='cai2yy', email='ss@nju.com', phone='12222222055', role_id=1)
    db.session.add(user1)
    db.session.commit()
    user = User.query.filter_by().first()
    return user.user_name + " : " + user.name


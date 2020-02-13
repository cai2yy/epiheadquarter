from flask import render_template, flash, redirect, url_for, Blueprint


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 用户权限判断
    return 1


@auth_bp.route('/logout')
def logout():
    return 1


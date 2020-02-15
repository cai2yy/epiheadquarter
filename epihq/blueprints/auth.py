from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from epihq.utils import redirect_back
from epihq.forms import LoginForm
from epihq.models import User

auth_bp = Blueprint('auth', __name__)


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
    return render_template('auth/indexTemp.html', form=form)


@auth_bp.route('/logout')
def logout():
    return "fuck you"
    # logout_user()
    # flash('Logout success.', 'info')
    # return redirect_back()


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


import random
from flask import render_template, flash, redirect, url_for, Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from epihq.utils import redirect_back
from epihq.forms import LoginForm,SettingForm,SignIn
from epihq.extensions import db, Swagger, swag_from
from epihq.models import User,Role

auth_bp = Blueprint('auth', __name__)


"""
注册&登录模块
@author: 
@time: 
"""


@auth_bp.route('/signIn', methods = ['GET', 'POST'])
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
            return  render_template('login.html',form = LoginForm())
        else:
            flash('参数有误请重新输入' )
    return render_template('auth/sign.html', form = form)


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


<<<<<<< HEAD
=======
"""
------------------以下为测试模块 -------------------------
"""


@auth_bp.route('/api/<string:language>/', methods=['GET'])
def hello_swagger1(language):
    """
        Test
        ---
        tags:
          - Test Swagger API
        parameters:
          - name: language
            in: path
            type: string
            required: true
            description: The language name
          - name: size
            in: query
            type: integer
            description: size of awesomeness
        responses:
          500:
            description: Error The language is not awesome!
          200:
            description: A language with its awesomeness
            schema:
              id: awesome
              properties:
                language:
                  type: string
                  description: The language name
                  default: Lua
                features:
                  type: array
                  description: The awesomeness list
                  items:
                    type: string
                  default: ["perfect", "simple", "lovely"]
        """

    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic",
        "simple", "powerful", "amazing",
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return "An error occurred, invalid language for awesomeness", 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
    )


@auth_bp.route('/hello/<string:word>')
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


@auth_bp.route('/sqltest')
def sql_test():
    db.drop_all()
    db.create_all()
    role1 = Role(name='管理员')
    role2 = Role(name='个人用户')
    role3 = Role(name='公司用户')
    db.session.add_all([role1,role2,role3])
    db.session.commit()

    user1 = User(username='user1', password='22', name='cai2yy', email='ss@nju.com', phone='12222222055', role_id=role1.id)
    user2 = User(username='user2', password='22', name='cai2yyy', email='ssyyy@nju.com', phone='122546522055',
                 role_id=role2.id)
    user3 = User(username='user3', password='22', name='cai2yyyy', email='ssyyyyyyy@nju.com', phone='12246465422055',
                 role_id=role2.id)
    db.session.add_all([user1,user2,user3])
    db.session.commit()
    testUserName = 'user1'
    user = db.session.query(User).filter_by(username = testUserName).first()

    return str(user.username )+ " : " + str(user.user_name)

>>>>>>> 85be84f893d933db21b4cab997573dd39bd6e2cc

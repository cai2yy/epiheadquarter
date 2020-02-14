from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from epihq.extensions import db
from epihq.const import ADMIN_USER, PERSON_USER, BUSINESS_USER


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    """
    users为用户表
    id为userid
    username为用户名
    password_hash为加密密码
    name为用户真实姓名
    useremail为用户邮箱
    userPhone为用户的手机
    role为用户角色，0代表管理员，1代表个人用户，2代表公司用户
    """
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    email = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    role_id = db.Column(db.Integer)


    def __init__(self, user_name, password, name, email, phone, role_id):
        self.user_name = user_name
        self.password_hash = generate_password_hash(password)
        self.name = name
        self.email = email
        self.phone = phone
        self.role_id = role_id

    def __repr__(self):
        return '<User %r>' % self.user_name


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def validate_admin(self):
        return self.role_id == ADMIN_USER

'''
class Article(db.Model):
    __tablename__ = 'articles'
    """
    article为新闻表
    id为新闻id
    news_title为新闻标题
    news_content为新闻内容
    news_time为新闻发表时间
    news_writer为新闻作者
    news_tag为新闻标签
    """
    id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.Text)
    article_content = db.Column(db.Text)
    article_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    article_writer = db.Column(db.String(20))
    article_tag = db.Column(db.String(20))


class Comment(db.Model):
    __tablename__ = 'comments'
    """
    comment为新闻评论表
    id为评论id
    comment_body为评论内容
    news_id为外键，指向News表中的id
    user_id为外键，指向user表中的id
    users和news为两个关联引用
    """
    id = db.Column(db.Integer, primary_key=True)
    comment_body = db.Column(db.Text)
    news_id = db.Column(db.Integer, db.ForeignKey('News.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    users = db.relationship('User', backref='comment')
    news = db.relationship('News', backref='comment')


class Role(db.Model):
    __tablename__ = 'roles'
    """
    Role为角色表
    id为角色id
    name为角色名，共有三类
    和users添加关系引用
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    users = db.relationship('User', backref='role')
'''
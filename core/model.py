from datetime import datetime
from flask_login import UserMixin

from werkzeug.security import generate_password_hash,check_password_hash
from core.extensions import db


'''
user为用户表
id为userid
username为用户名
password_hash为加密密码
name为用户真实姓名
useremail为用户邮箱
userPhone为用户的手机
role为用户角色，1代表管理员，2代表个人用户，3代表公司用户
'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    useremail = db.Column(db.String(30))
    userPhone = db.Column(db.Integer)
    role_id = db.Column(db.Integer,db.ForeignKey('Role.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

'''
news为新闻表
id为新闻id
news_title为新闻标题
news_content为新闻内容
news_time为新闻发表时间
news_writer为新闻作者
news_tag为新闻类别
'''
class News(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    news_title = db.Column(db.Text)
    news_content = db.Column(db.Text)
    news_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    news_writer = db.Column(db.String(20))
    news_tag = db.Column(db.String(20))


'''
comment为新闻评论表
id为评论id
comment_body为评论内容
news_id为外键，指向News表中的id
user_id为外键，指向user表中的id
users和news为两个关联引用
'''
class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    comment_body = db.Column(db.Text)
    news_id = db.Column(db.Integer,db.ForeignKey('News.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('User.id'))
    users = db.relationship('User',backref = 'comment')
    news = db.relationship('News',backref = 'comment')

'''
Role为角色表
id为角色id
name为角色名，共有三类
和users添加关系引用
'''
class Role(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)
    users = db.relationship('User',backref = 'role')


from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from epihq.extensions import db
from epihq.const import ADMIN_USER, PERSON_USER, BUSINESS_USER


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    """
    用户表
    id为用户id
    username为用户名
    password_hash为加密密码
    name为用户真实姓名
    user_email为用户邮箱
    userPhone为用户的手机
    role为用户角色，0代表管理员，1代表个人用户，2代表公司用户
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    user_name = db.Column(db.String(30))
    user_email = db.Column(db.String(30))
    user_Phone = db.Column(db.String(30))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    users_relate_roles = db.relationship('Role', backref='roles_relate_users')

    def __init__(self, username, password, name, email, phone, role_id):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.name = name
        self.email = email
        self.phone = phone
        self.role_id = role_id

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def validate_admin(self):
        return self.role_id == ADMIN_USER


class Article(db.Model):
    __tablename__ = 'articles'
    """
    新闻表
    id为新闻id
    article_title为新闻标题
    article_content为新闻内容
    article_time为新闻发表时间
    article_writer为新闻作者
    article_tag为新闻标签
    """
    id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.Text)
    article_content = db.Column(db.Text)
    article_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    article_writer = db.Column(db.String(20))
    article_tag = db.Column(db.String(20))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Mark(db.Model):
    __tablename__ = 'marks'
    """
    收藏表，是users-articles的一个连接表
    id为收藏项id
    article_id为外键，指向articles表中的id
    user_id为外键，指向user表中的id
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    marks_relate_users = db.relationship('User', backref='users_relate_marks')
    marks_relate_articles = db.relationship('Article', backref='articles_relate_marks')

    def __init__(self, user_id, article_id):
        self.user_id = user_id
        self.article_id = article_id


class Comment(db.Model):
    __tablename__ = 'comments'
    """
    新闻评论表
    id为评论id
    comment_body为评论内容
    article_id为外键，指向articles表中的id
    user_id为外键，指向user表中的id
    users和news为两个关联引用
    """
    id = db.Column(db.Integer, primary_key=True)
    comment_body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    comments_relate_users = db.relationship('User', backref='users_relate_comments')
    comments_relate_articles = db.relationship('Article', backref='articles_relate_comments')


class Role(db.Model):
    __tablename__ = 'roles'
    """
    角色表
    id为角色id
    name为角色名，共有三类
    和users添加关系引用
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)


class NLP(db.Model):
    __tablename__ = 'nlp'
    """
    用户-NLP程序表 1 <-> 1
    description为用户添加的备注
    user_id为外键，指向user表中的id
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    nlp_relate_users = db.relationship('User', backref='users_relate_nlp')


class TrainSet(db.Model):
    __tablename__ = 'train_sets'
    """
    NLP程序-训练集表 1 <-> N
    set_content为用户上传的训练集
    nlp_id为外键，指向nlp表中的id
    """
    id = db.Column(db.Integer, primary_key=True)
    set_name = db.Column(db.String(20))
    set_content = db.Column(db.Text)
    nlp_id = db.Column(db.Integer, db.ForeignKey('nlp.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    sets_relate_nlp = db.relationship('NLP', backref='nlp_relate_sets')


class TrainResult(db.Model):
    # todo 待完善
    __tablename__ = 'train_results'
    """
    NLP程序-训练结果表 1 <-> N
    title为标题
    text为文本
    entities为实体集，即实体标签
    tags为标签
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    text = db.Column(db.Text)
    entities = db.Column(db.String(20))
    tags = db.Column(db.String(20))
    nlp_id = db.Column(db.Integer, db.ForeignKey('nlp.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    results_relate_nlp = db.relationship('NLP', backref='nlp_relate_results')

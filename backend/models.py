from datetime import datetime
from flask import url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from utils.extensions import db
from utils.const import ADMIN_USER


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # 如果当前没有任何资源时，或者前端请求的 page 越界时，都会抛出 404 错误
        # 由 @bp.app_errorhandler(404) 自动处理，即响应 JSON 数据：{ error: "Not Found" }
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

    def to_dict(self):
        return {
            c.name: getattr(User, c.name) for c in self.__table__.columns
        }


class User(db.Model, UserMixin, PaginatedAPIMixin):
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
    user_phone = db.Column(db.String(30))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    users_relate_roles = db.relationship('Role', backref='roles_relate_users')

    def __init__(self, username, password, name, email, phone, role_id):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.user_name = name
        self.user_email = email
        self.user_phone = phone
        self.role_id = role_id

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def validate_admin(self):
        return self.role_id == ADMIN_USER


class Article(db.Model, PaginatedAPIMixin):
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
    article_author = db.Column(db.String(20))
    article_tag = db.Column(db.String(20))
    top = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def from_dict(self, data):
        for field in ['title', 'content', 'time', 'author', 'tag']:
            if field in data:
                setattr(self, field, data[field])


class Mark(db.Model, PaginatedAPIMixin):
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


class Comment(db.Model, PaginatedAPIMixin):
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

    def __init__(self, body, user_id, article_id):
        self.comment_body = body
        self.user_id = user_id
        self.article_id = article_id


class Role(db.Model):
    __tablename__ = 'roles'
    """
    角色表
    id为角色id
    id:     0     |    1    |    2  
    name: 管理员  | 个人用户 | 企业用户
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    def __init__(self, role_id, name):
        self.id = role_id
        self.name = name


class NLP(db.Model, PaginatedAPIMixin):
    __tablename__ = 'nlp'
    """
    用户-NLP程序表 1 <-> N
    description为用户添加的备注
    user_id为外键，指向user表中的id
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    nlp_relate_users = db.relationship('User', backref='users_relate_nlp')


class TrainSet(db.Model, PaginatedAPIMixin):
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


class TrainResult(db.Model, PaginatedAPIMixin):
    # todo 待完善
    __tablename__ = 'train_results'
    """
    NLP程序-训练结果表 1 <-> N
    title为标题
    text为文本
    status为训练状态，0->未开始，1->正在训练,2->训练结束
    entities为实体集，即实体标签
    tags为标签
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    text = db.Column(db.Text)
    entities = db.Column(db.String(20))
    tags = db.Column(db.String(20))
    status = db.Column(db.Integer, db.ForeignKey('train_status.id'), default=0)
    nlp_id = db.Column(db.Integer, db.ForeignKey('nlp.id'))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    results_relate_status = db.relationship('TrainStatus', backref='status_relate_results')
    results_relate_nlp = db.relationship('NLP', backref='nlp_relate_results')

    def __init__(self, title, text, nlp_id):
        self.title = title
        self.text = text
        self.nlp_id = nlp_id


class TrainStatus(db.Model):
    __tablename__ = 'train_status'
    """
    训练状态表
    id:     0     |    1    |   2  
    name: 未开始  | 正在运行 | 已完成
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    def __init__(self, status_id, name):
        self.id = status_id
        self.name = name

from flask import render_template, redirect, url_for, Blueprint, make_response, jsonify
from backend.models import User, Role, TrainStatus
from backend.utils.extensions import db, swag_from
from backend.utils.helper import redirect_back

manager_bp = Blueprint('manager', __name__)


"""
------------------ 留待第二次迭代 ------------------
"""


"""
------------------ 以下为测试模块 ------------------
"""


@manager_bp.route('/hello')
def hello():
    """
        helloWorld
        ---
        tags:
            - 测试
    """
    return make_response(jsonify('hello, world!'), 200)


@manager_bp.route('/sql/init')
def create_tables():
    """
        数据库初始化API
        ---
        tags:
            - 测试
        description: 访问该API初始化数据库表和完成2个状态表的插入
    """
    db.create_all()
    role = Role.query.filter_by(id=0).first()
    if not role:
        role = Role(1, 'ADMIN')
        db.session.add(role)
        role = Role(2, 'PERSON')
        db.session.add(role)
        role = Role(3, 'BUSINESS')
        db.session.add(role)
    status = TrainStatus.query.filter_by(id=0).first()
    """初始化训练状态表"""
    if not status:
        status = TrainStatus(1, 'READY')
        db.session.add(status)
        status = TrainStatus(2, 'RUNNING')
        db.session.add(status)
        status = TrainStatus(3, 'FINISHED')
        db.session.add(status)
    db.session.commit()
    return make_response('创建成功', 200)

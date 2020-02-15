import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
import click

from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from epihq.blueprints.user import user_bp
from epihq.blueprints.auth import auth_bp
from epihq.blueprints.news import news_bp
from epihq.blueprints.manager import manager_bp
from epihq.blueprints.map import map_bp
from epihq.extensions import bootstrap, db, login_manager, csrf, ckeditor, mail, moment, toolbar, migrate, swagger
from epihq.models import User
from epihq.config import config, SQLALCHEMY_DATABASE_URI
from epihq.crawler import async_get_articles, async_get_patients_data
from epihq.const import ADMIN_USER, PERSON_USER, BUSINESS_USER

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(2)

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('epihq')
    # 连接本地数据库，测试临时用
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
    # register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    # register_errors(app)
    register_shell_context(app)
    # register_template_context(app)
    register_request_handlers(app)
    register_crawler(app)
    return app


def register_crawler(app):
    """开两个事件循环,分别抓取文章和疫情数据"""
    executor.submit(async_get_articles)
    executor.submit(async_get_patients_data)


def register_extensions(app):
    """加载工具模块"""
    bootstrap.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)


def register_blueprints(app):
    """加载功能模块"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(map_bp)


def register_logging(app):
    """加载日志功能"""
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/bluelog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='Bluelog Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)


def register_template_context(app):
    """上下文处理器，注入dict映射使之所有的Templates中可见"""
    @app.context_processor
    def init_template_context():
        admin = User.query.filter_by().first(role_id=0)
        if current_user.is_authenticated:
            articles = None
        else:
            articles = None
        return dict(
            admin=admin, articles=articles)


def register_shell_context(app):
    """在使用命令行启动程序时调用函数，注入dict映射使之在shell中可见"""
    @app.shell_context_processor
    def init_shell_context():
        return dict(db=db, User=User, Article=Article, Comment=Comment, Role=Role)


def register_commands(app):
    """在使用命令行启动程序时，通过附加参数调用该函数"""
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    # 使用举例(在命令行中): >python xx.py --drop
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')


def register_errors(app):
    """网络请求发生错误时调用函数"""
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_request_handlers(app):
    """网络请求被正确执行后调用该函数"""
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= app.config['EPIHQLOG_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response

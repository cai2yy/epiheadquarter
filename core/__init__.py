import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from core.blueprints.user import user_bp
from core.blueprints.auth import auth_bp
from core.blueprints.news import news_bp

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == "__main__":
    app.run()
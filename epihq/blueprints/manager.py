from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user
from epihq.models import User, Article, Comment, Role
from epihq.extensions import db
from epihq.forms import CommentForm
from epihq.utils import redirect_back

manager_bp = Blueprint('manager', __name__)


@manager_bp.route('/manager')
def home_article():
    return render_template('manager/home.html')

from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user
from epihq.models import User, Article, Comment, Role
from epihq.extensions import db
from epihq.forms import CommentForm
from epihq.utils import redirect_back

map_bp = Blueprint('map', __name__)


@map_bp.route('/')
def index():
    return render_template('index.html')


@map_bp.route('/map')
def home_map():
    return render_template('index.html')

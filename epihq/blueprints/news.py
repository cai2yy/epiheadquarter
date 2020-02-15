from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user
from epihq.models import User, Article, Comment, Role
from epihq.extensions import db
from epihq.forms import CommentForm
from epihq.utils import redirect_back

news_bp = Blueprint('news', __name__)


@news_bp.route('/news')
def home_article():
    return render_template('news/home.html')


@news_bp.route('/news/<int:article_id>')
def show_article(article_id):
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect('/login')


@news_bp.route('/train/<int:article_id>')
def train(article_id):
    # 公司用户权限
    # 对该文章进行训练，训练结果在用户页面查看
    return 1


@news_bp.route('/article/delete/<int:article_id>')
def delete_article(article_id):
    """用户是否登录"""
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect('/login')
    user = current_user
    """用户是否为管理员"""
    if not user.validate_admin:
        flash('没有该权限')
    else:
        article = Article.query.filter_by(id=article_id).first()
        db.session.delete(article)
        db.session.commit()
        flash("删除文章成功")
        return render_template('news/home')


@news_bp.route('/article/stick/<int:article_id>')
def stick_article(article_id):
    # 管理员用户权限
    # 置顶文章
    return 1


@news_bp.route('/article/mark/<int:article_id>')
def mark(article_id):
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect('/login')
    user = current_user
    article = Article.query.filter_by(article_id=article_id).update({'marked': True})
    db.session.commit()
    render_template('article/show.html')

@news_bp.route('/article/mark/<int:article_id>')
def cancel_mark(article_id):
    # 普通用户权限
    # 取消收藏文章
    return 1


@news_bp.route('/comment/delete/<int:comment_id>')
def delete_comment(comment_id):
    # 删除评论
    return 1


@news_bp.route('/article/reply/<int:article_id>')
def post_comment(article_id):
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect('/login')
    form = CommentForm()
    if form.validate_on_submit():
        comment_content = form.body
        user = current_user
        comment = Comment(comment_body=comment_content, user_id=user.id, user_name=user.name, article_id=article_id)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('.post_comment', article_id=article_id))

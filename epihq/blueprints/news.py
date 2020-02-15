from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user
from epihq.models import User, Article, Comment, Role
from epihq.extensions import db
from epihq.forms import CommentForm
from epihq.utils import redirect_back

news_bp = Blueprint('news', __name__)


"""
文章模块
@author: 
@time: 
"""


@news_bp.route('/news')
def home_article():
    # todo 新闻首页
    return render_template('news/home.html')


@news_bp.route('/news/<int:article_id>')
def show_article(article_id):
    # todo 文章页面
    return render_template('news/article.html')


@news_bp.route('/news/mark/<int:article_id>')
def mark_article(article_id):
    # todo 收藏文章
    return redirect_back()


@news_bp.route('/article/remark/<int:article_id>')
def remark_article(article_id):
    # todo 取消收藏
    return redirect_back()


@news_bp.route('/news/add/<int:article_id>')
def add_task(article_id):
    # todo 将文章加入任务列表（启动任务在user模块）
    return redirect_back()


@news_bp.route('/news/delete/<int:article_id>')
def delete_article(article_id):
    """用户是否登录"""
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect(url_for('auth.login'))
    user = current_user
    """用户是否为管理员"""
    if not user.validate_admin:
        flash('没有该权限')
        return redirect_back()
    Article.query.filter_by(id=article_id).delete()
    db.session.commit()
    flash("删除文章成功")
    return redirect_back(url_for('.home_article'))


@news_bp.route('/news/stick/<int:article_id>')
def stick_article(article_id):
    # todo 置顶文章
    return redirect_back()


@news_bp.route('/news/destick/<int:article_id>')
def cancel_stick_article(article_id):
    # todo 取消置顶文章
    return redirect_back()


"""
评论模块
@author: 
@time: 
"""


@news_bp.route('/news/comment/<int:article_id>')
def post_comment(article_id):
    # todo 评论文章
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
    return redirect_back()


@news_bp.route('/comment/reply/<int:comment_id>')
def reply_comment(comment_id):
    # todo 回复评论
    return redirect_back()


@news_bp.route('/comment/delete/<int:comment_id>')
def delete_comment(comment_id):
    # todo 删除评论
    return redirect_back()


"""
分享模块
@author: 
@time: 
"""


@news_bp.route('/article/share/<int:article_id>')
def share_article(article_id):
    # todo 分享功能，这个目测比较难
    return redirect_back()


from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user
from epihq.models import User, Article, Comment, Role, Mark
from epihq.extensions import db
from epihq.forms import CommentForm
from epihq.utils import redirect_back
from json import dumps

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
    """
        文章阅读页API
        ---
        parameters:
          - name: user_id
            in: path
            type: integer
            required: true
            description: 用户id
          - name: article_id
            in: path
            type: integer
            required: true
            description: 文章id
    """
    article = Article.query.filter_by(id=article_id).first()
    article_json = dumps(article)
    comments = Comment.query.filter_by(article_id=article_id)
    comments_json = dumps(comments)
    return render_template('news/article.html', article=article_json, comments=comments_json)


@news_bp.route('/news/mark/<int:user_id>/<int:article_id>')
def mark_article(user_id, article_id):
    """
        收藏文章API
        ---
        parameters:
          - name: user_id
            in: path
            type: integer
            required: true
            description: 用户id
          - name: article_id
            in: path
            type: integer
            required: true
            description: 文章id
    """
    mark = Mark.query.filter_by(user_id=user_id, article_id=article_id).first()
    if mark is None:
        mark = Mark(user_id, article_id)
        db.session.add(mark)
    else:
        Mark.query.filter_by(user_id=user_id, article_id=article_id).delete()
    db.session.commit()
    db.session.close()
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

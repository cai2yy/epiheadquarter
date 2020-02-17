from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user
from epihq.models import User, Article, Comment, Role, Mark, TrainResult, TrainSet, NLP
from epihq.extensions import db
from epihq.forms import CommentForm
from epihq.utils import redirect_back
from epihq.const import PERSON_USER
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


@news_bp.route('/news/<int:article_id>', methods=['GET'])
def show_article(article_id):
    """
            获取文章API
            ---
            parameters:
              - name: article_id
                in: path
                type: integer
                required: true
                description: 文章id
        """
    article = Article.query.filter_by(id=article_id).first()
    if article is None:
        flash("文章不存在或已被删除")
        abort(404)
    article_json = dumps(article)
    comments = Comment.query.filter_by(article_id=article_id)
    comments_json = dumps(comments)
    return render_template('news/show_article.html', article=article_json, comments=comments_json)


@news_bp.route('/news/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """
            删除文章API
            ---
            parameters:
              - name: article_id
                in: path
                type: integer
                required: true
                description: 文章id
        """
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect('/login')
    user = current_user
    if not user.validate_admin:
        flash('没有该权限')
        return redirect_back()
    Article.query.filter_by(id=article_id).delete()
    db.session.commit()
    flash("删除文章成功")
    return redirect_back()


@news_bp.route('/news/mark/<int:article_id>')
def mark_article(article_id):
    """
            收藏文章API
            ---
            parameters:
              - name: article_id
                in: path
                type: integer
                required: true
                description: 文章id
        """
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect('/login')
    user_id = current_user.id
    mark = Mark.query.filter_by(user_id=user_id, article_id=article_id).first()
    if mark is None:
        mark = Mark(user_id, article_id)
        db.session.add(mark)
    else:
        Mark.query.filter_by(user_id=user_id, article_id=article_id).delete()
    db.session.commit()
    db.session.close()
    return redirect_back()


@news_bp.route('/news/train/<int:article_id>')
def task_article(article_id, nlp_id):
    """
            将文章添加到训练任务队列API
            ---
            parameters:
              - name: article_id
                in: path
                type: integer
                required: true
                description: 当前文章id
              - name: nlp_id
                in: query
                type: integer
                required: true
                description: 单击'添加任务'按钮后弹出nlp单选框（陈列了该用户创建的nlp)，用户选中项提交了该参数
        """
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect('/login')
    article = Article.query.filter_by(article_id=article_id).first()
    result = TrainResult(article.article_title, article.article_content, nlp_id)
    db.session.add(result)
    db.session.commit()
    return redirect_back()


@news_bp.route('/news/top/<int:article_id>')
def top_article(article_id):
    """
                置顶文章API，需要管理员权限
                ---
                parameters:
                  - name: article_id
                    in: path
                    type: integer
                    required: true
                    description: 当前文章id
            """
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

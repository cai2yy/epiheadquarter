from flask import render_template, flash, redirect, Blueprint, abort, url_for, jsonify, request, current_app, make_response
from flask_login import current_user
from backend.models import Article, Comment, Mark, TrainResult
from utils.extensions import db, swag_from
from backend.forms import CommentForm
from utils.helper import redirect_back
from json import dumps

news_bp = Blueprint('news', __name__)


"""
文章模块
@author: 
@time: 
"""


@news_bp.route('/news', methods=['GET'])
def show_articles():
    """
    获取全部文章-分页显示
    ---
    tags:
      - 文章
    responses:
      '200':
        description: 获取文章成功
        schema:
          $ref: '#/definitions/responses/ArticleCollection'
    """
    pages_num = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get('per_page', current_app.config['MESSAGES_PER_PAGE'], type=int), 20)
    data = Article.to_collection_dict(
        Article.query.order_by(Article.timestamp.desc()), pages_num, per_page, 'api.get_article')
    return jsonify(data)


@news_bp.route('/news/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """
    获取文章
    ---
    tags:
      - 文章
    parameters:
      - name: article_id
        description: 文章id
        in: path
        required: true
        type: integer
    responses:
      '200':
        description: 获取文章成功
        schema:
          $ref: '#/definitions/responses/Article'
    """
    article = Article.query.filter_by(id=article_id).first()
    if article is None:
        flash("文章不存在或已被删除")
        abort(404)
    comments = Comment.query.filter_by(article_id=article_id)
    """是否登录flag变量"""
    is_login = current_user.is_authenticated
    return make_response(jsonify({'article': article, 'comments': comments, 'is_login': is_login}), 200)


@news_bp.route('/news/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    """
    编辑文章
    ---
    tags:
      - 文章
    parameters:
      - name: article_id
        description: 文章id
        in: path
        required: true
        type: integer
      - name: Comment
        description: 文章表单
        in: body
        required: true
        schema:
          $ref: '#/definitions/parameters/Article'
    responses:
      '200':
        description: 编辑文章成功
      '403':
        description: 没有该权限
      '404':
        description: 文章不存在
    """
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect(url_for('auth.login'))
    user = current_user
    if not user.validate_admin:
        flash('没有该权限')
        return make_response("no permission", 403)
    article = Article.query.get_or_404(id=article_id)
    edit_article = request.form.to_dict()
    if not edit_article:
        return make_response("article does not exist", 404)
    article.from_dict(edit_article)
    db.session.commit()
    flash("编辑文章成功")
    return make_response("modified successfully", 200)


@news_bp.route('/news/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """
    删除文章
    ---
    tags:
      - 文章
    parameters:
      - name: article_id
        description: 文章id
        in: path
        required: true
        type: integer
    responses:
      '200':
        description: 删除文章成功
      '403':
        description: 没有该权限
    """
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect(url_for('auth.login'))
    user = current_user
    if not user.validate_admin:
        flash('没有该权限')
        return make_response("no permission", 403)
    Article.query.filter_by(id=article_id).delete()
    db.session.commit()
    flash("删除文章成功")
    return make_response("deleted successfully", 200)


@news_bp.route('/news/mark/<int:article_id>', methods=['GET'])
def mark_article(article_id):
    """
    收藏/取消收藏文章
    ---
    tags:
      - 文章
    parameters:
      - name: article_id
        description: 文章id
        in: path
        required: true
        type: integer
    responses:
      '200':
        description: 成功收藏/取消收藏
    """
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect(url_for('auth.login'))
    user_id = current_user.id
    mark = Mark.query.filter_by(user_id=user_id, article_id=article_id).first()
    if mark is None:
        mark = Mark(user_id, article_id)
        db.session.add(mark)
        db.session.commit()
        return make_response("marked successfully", 200)
    Mark.query.filter_by(user_id=user_id, article_id=article_id).delete()
    db.session.commit()
    return make_response("unmarked successfully", 200)


@news_bp.route('/news/train/<int:article_id>', methods=['GET'])
def train_article(article_id, nlp_id):
    """
        添加文章到训练队列
        ---
        tags:
          - 训练
        parameters:
          - name: article_id
            description: 文章id
            in: path
            required: true
            type: integer
        responses:
          '200':
            description: 收藏成功/失败
        """
    if current_user.is_anonymous:
        flash('请先登录')
        return redirect(url_for('auth.login'))
    article = Article.query.filter_by(article_id=article_id).first()
    result = TrainResult(article.article_title, article.article_content, nlp_id)
    db.session.add(result)
    db.session.commit()
    return make_response("successfully added article to task queue", 200)


@news_bp.route('/news/top/<int:article_id>')
def top_article(article_id):
    """
    置顶/取消置顶文章
    ---
    tags:
      - 文章
    parameters:
      - name: article_id
        description: 文章id
        in: path
        required: true
        type: integer
    responses:
      '200':
        description: 成功置顶/取消置顶
    """
    is_top = Article.query.filter_by(article_id=article_id).first().top
    if is_top:
        Article.query.filter_by(article_id=article_id).first().update(top=False)
        db.session.commit()
        return make_response("successfully cancel top article", 200)
    Article.query.filter_by(article_id=article_id).first().update(top=True)
    db.session.commit()
    return make_response("successfully top article", 200)


"""
评论模块
@author: 
@time: 
"""


@news_bp.route('/news/comment/<int:article_id>', methods=['POST'])
@swag_from('../apidocs/post_comment.yml')
def post_comment(article_id):
    data = request.form.to_dict()
    comment_content = data['body']
    user = current_user
    comment = Comment(body=comment_content, user_id=user.id, article_id=article_id)
    db.session.add(comment)
    db.session.commit()
    resp = make_response(jsonify(data), 201)
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    resp.headers['Location'] = 'comment/' + str(comment.id)
    return resp


@news_bp.route('/comment/<int:comment_id>', methods=['GET'])
@swag_from('../apidocs/get_comment.yml')
def get_comment(comment_id):
    comment = Comment.query.get_or_404(id=comment_id)
    db.session.add(comment)
    db.session.commit()
    return make_response(jsonify(comment.to_dict()), 200)


@news_bp.route('/comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """
        删除评论API
        ---
        tags:
          - 评论
        parameters:
          - name: comment_id
            in: path
            type: integer
            required: true
            description: 评论id
        responses:
            '200':
                description: 删除成功
    """
    Comment.query.filter_by(comment_id=comment_id).delete()
    db.session.commit()
    return make_response("deleted successfully", 200)


"""
分享模块
@author: 
@time: 
"""


@news_bp.route('/article/share/<int:article_id>')
def share_article(article_id):
    # todo 分享功能
    return redirect_back()

from flask import render_template, flash, redirect, url_for, Blueprint

news_bp = Blueprint('news', __name__)


@news_bp.route('/train/<int:article_id>')
def train(article_id):
    # 公司用户权限
    # 对该文章进行训练，训练结果在用户页面查看
    return 1


@news_bp.route('/article/delete/<int:article_id>')
def delete_article(article_id):
    # 管理员用户权限
    # 删除文章
    return 1


@news_bp.route('/article/stick/<int:article_id>')
def stick_article(article_id):
    # 管理员用户权限
    # 置顶文章
    return 1


@news_bp.route('/article/mark/<int:article_id>')
def mark(article_id):
    # 普通用户权限
    # 收藏文章
    return 1


@news_bp.route('/article/mark/<int:article_id>')
def cancel_mark(article_id):
    # 普通用户权限
    # 取消收藏文章
    return 1


@news_bp.route('/comment/delete/<int:comment_id>')
def delete_comment(comment_id):
    # 管理员用户权限
    # 删除评论
    return 1


@news_bp.route('/comment/reply/<int:article_id>')
def post_comment(article_id):
    # 普通用户权限
    # 发表评论
    return 1
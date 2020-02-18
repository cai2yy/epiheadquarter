from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, HiddenField, \
    BooleanField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, EqualTo


class LoginForm(FlaskForm):
    """继承了FlaskForm（表单工具类）类"""
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()


class CommentForm(FlaskForm):
    # 待补充验证码功能
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    # 注册表单
    # 以下各个参数为
    username = StringField('用户名', validators=[DataRequired(), Length(1, 30)])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 30)])
    passwordConFirm = PasswordField('确认密码', validators=[DataRequired(), Length(6,30), EqualTo('password')])
    user_name = StringField('您的真实姓名', validators=[DataRequired(), Length(1, 30)])
    user_phone = StringField('电话', validators=[DataRequired(), Length(11)])
    user_email = StringField('邮箱', validators=[DataRequired(), Email()])
    roleLevel = StringField('用户级别', validators=[DataRequired()])
    submit = SubmitField('注册')



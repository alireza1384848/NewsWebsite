

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email

class SignupForm(FlaskForm):
    username = StringField(label='نام کاربری:', validators=[DataRequired()])
    email = StringField(label='ایمیل :', validators=[DataRequired(), Email(message="ایمیل شما نامعتبر است!")])
    password = PasswordField(label='رمز عبور :', validators=[DataRequired()])
    national_key = PasswordField(label='کد ملی :', validators=[DataRequired()])
    confirm_password = PasswordField(label='تایید رمز عبور :', validators=[DataRequired(), EqualTo('password', message='تایید رمز عبور با رمز عبور یکسان نیست!')])
    remember = BooleanField('مرا به خاطر بسپار')
    submit = SubmitField(label='ثبت نام')

class LoginForm(FlaskForm):
    username = StringField(label='نام کاربری :', validators=[DataRequired()])
    password = PasswordField(label='رمز عبور :', validators=[DataRequired()])
    remember = BooleanField('مرا به خاطر بسپار')
    submit = SubmitField(label='ورود')
class AddNewsForm(FlaskForm):
    author = StringField(label="نام نویسنده", validators=[DataRequired()])
    image_url = StringField(label="لینک تصویر", validators=[DataRequired()])
    date = StringField(label="تاریخ نوشته", validators=[DataRequired()])
    title = StringField(label="عنوان", validators=[DataRequired()])
    summary = TextAreaField(label="خلاصه از خبر", validators=[DataRequired()])
    body = TextAreaField(label="خلاصه از متن کامل خبر ", validators=[DataRequired()])
    submit = SubmitField('ثبت خبر')
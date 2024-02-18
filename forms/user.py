from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    surname = StringField('surname', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    login = StringField('login', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

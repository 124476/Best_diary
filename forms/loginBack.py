from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class LoginLoginBack(FlaskForm):
    password = StringField('Новый пароль', validators=[DataRequired()])
    submit = SubmitField('Изменить')

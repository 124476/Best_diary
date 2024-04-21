from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class LoginPasswordBack(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    submit = SubmitField('Восстановить')

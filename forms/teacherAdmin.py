from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegisterFormTeacherAdmin(FlaskForm):
    login = StringField('Логин учителя:', validators=[DataRequired()])
    submit = SubmitField('Добавить')

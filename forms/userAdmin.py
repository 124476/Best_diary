from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegisterFormUserAdmin(FlaskForm):
    login = StringField('Логин ученика:', validators=[DataRequired()])
    submit = SubmitField('Добавить')

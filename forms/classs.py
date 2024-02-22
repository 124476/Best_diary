from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegisterFormClass(FlaskForm):
    name = StringField('Название класса:', validators=[DataRequired()])
    submit = SubmitField('Добавить')

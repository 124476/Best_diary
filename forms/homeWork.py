from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class RegisterFormHomeWork(FlaskForm):
    textDz = TextAreaField('Текст:', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

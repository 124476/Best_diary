from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class RegisterFormTeacherClass(FlaskForm):
    login = IntegerField('Id класса:', validators=[DataRequired()])
    predmet = IntegerField('Id предмета:', validators=[DataRequired()])
    submit = SubmitField('Добавить')

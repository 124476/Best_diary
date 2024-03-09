from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class RegisterFormTeacherClass(FlaskForm):
    login = StringField('Id класса:', validators=[DataRequired()])
    predmet = StringField('Id предмета:', validators=[DataRequired()])
    submit = SubmitField('Добавить')

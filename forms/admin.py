from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterFormAdmin(FlaskForm):
    surname = StringField('Фамилия директора:', validators=[DataRequired()])
    name = StringField('Имя директора:', validators=[DataRequired()])
    school = StringField('Название школы:', validators=[DataRequired()])
    login = StringField('Логин:', validators=[DataRequired()])
    email = EmailField('Почта:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

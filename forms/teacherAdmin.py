from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterFormTeacherAdmin(FlaskForm):
    login = StringField('Логин учителя:', validators=[DataRequired()])
    submit = SubmitField('Добавить')

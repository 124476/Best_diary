from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class RegisterFormEvaluation(FlaskForm):
    name = StringField('Название события:', validators=[DataRequired()])
    type = IntegerField('Оценка:', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class RegisterFormHomeWork(FlaskForm):
    textDz = TextAreaField('Текст:', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

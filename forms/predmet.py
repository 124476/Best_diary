from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class RegisterFormEvaluation(FlaskForm):
    name = StringField('Название события:', validators=[DataRequired()])
    type = IntegerField('Оценка:', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

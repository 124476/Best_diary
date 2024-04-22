from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginPasswordBack(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    submit = SubmitField('Восстановить')

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginLoginBack(FlaskForm):
    password = StringField('Новый пароль', validators=[DataRequired()])
    submit = SubmitField('Изменить')

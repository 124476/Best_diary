from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterFormClass(FlaskForm):
    name = StringField('Название класса:', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

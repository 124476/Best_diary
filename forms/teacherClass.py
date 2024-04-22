from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired


class RegisterFormTeacherClass(FlaskForm):
    login = IntegerField('Название класса:', validators=[DataRequired()])
    predmet = IntegerField('Id предмета:', validators=[DataRequired()])
    submit = SubmitField('Добавить')

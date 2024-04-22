import sqlalchemy
from flask_login import UserMixin

from data.db_session import SqlAlchemyBase


class PredmetAndTeacher(SqlAlchemyBase, UserMixin):
    __tablename__ = 'predmetAndTeachers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    idPredmet = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    idClass = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    idTeacher = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

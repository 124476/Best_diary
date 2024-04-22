import sqlalchemy
from flask_login import UserMixin

from data.db_session import SqlAlchemyBase


class Evaluation(SqlAlchemyBase, UserMixin):
    __tablename__ = 'evaluations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    idUser = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    idPredmet = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    idTeacher = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)


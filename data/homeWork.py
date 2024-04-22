import sqlalchemy
from flask_login import UserMixin

from data.db_session import SqlAlchemyBase


class HomeWork(SqlAlchemyBase, UserMixin):
    __tablename__ = 'homeWorks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    predmetId = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    classId = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    teacherId = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    textDz = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

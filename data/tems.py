import sqlalchemy
from flask_login import UserMixin

from data.db_session import SqlAlchemyBase


class Tems(SqlAlchemyBase, UserMixin):
    __tablename__ = 'tems'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.TEXT, nullable=True)

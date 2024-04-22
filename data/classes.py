import sqlalchemy
from flask_login import UserMixin

from data.db_session import SqlAlchemyBase


class Classs(SqlAlchemyBase, UserMixin):
    __tablename__ = 'classes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adminId = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

import sqlalchemy
from flask_login import UserMixin

from data.db_session import SqlAlchemyBase


class Predmet(SqlAlchemyBase, UserMixin):
    __tablename__ = 'predmets'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

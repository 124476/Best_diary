import datetime
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Evaluation(SqlAlchemyBase, UserMixin):
    __tablename__ = 'evaluations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    nameType = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    userId = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    teacherId = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    nameClass = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    nameObject = sqlalchemy.Column(sqlalchemy.String, nullable=True)

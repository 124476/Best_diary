from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.teachers import Teacher

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('login', required=True)
parser.add_argument('email', required=True)


def abort_if_news_not_found(teacher_login):
    session = db_session.create_session()
    users = session.query(Teacher).get(teacher_login)
    if not users:
        abort(404, message=f"Teacher {teacher_login} not found")


class TeachersResource(Resource):
    def get(self, teacher_login):
        abort_if_news_not_found(teacher_login)
        session = db_session.create_session()
        teacher = session.query(Teacher).filter(teacher_login == Teacher.login).first()
        return jsonify({
            'teacher':
                {'surname': teacher.surname,
                 'name': teacher.name,
                 'login': teacher.login,
                 'email': teacher.email}
        })


class TeachersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        teachers = session.query(Teacher).all()
        return jsonify({
            'teachers':
                [{'surname': item.surname,
                  'name': item.name,
                  'login': item.login,
                  'email': item.email} for item in teachers]
        })

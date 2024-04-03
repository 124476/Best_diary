from flask import Flask, render_template, redirect, make_response, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.users import User

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('login', required=True)
parser.add_argument('email', required=True)


def abort_if_news_not_found(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        abort(404, message=f"Users {users_id} not found")


class UsersResource(Resource):
    def get(self, user_login):
        abort_if_news_not_found(user_login)
        session = db_session.create_session()
        user = session.query(User).filter(user_login == User.login).first()
        return jsonify({
            'user':
                {'surname': user.surname,
                 'name': user.name,
                 'login': user.login,
                 'email': user.email}
        })


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            'users':
                [{'surname': item.surname,
                  'name': item.name,
                  'login': item.login,
                  'email': item.email} for item in users]
        })

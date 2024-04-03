import flask
from flask import jsonify

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users':
                [{'surname': item.surname,
                  'name': item.name,
                  'login': item.login,
                  'email': item.email} for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_login>', methods=['GET'])
def get_one_users(user_login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(user_login == User.login).first()
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user':
                {'surname': user.surname,
                 'name': user.name,
                 'login': user.login,
                 'email': user.email}
        }
    )

import flask
from flask import jsonify

from data import db_session
from data.teachers import Teacher

blueprint = flask.Blueprint(
    'teachers_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/teachers')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(Teacher).all()
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'teachers':
                [{'surname': item.surname,
                  'name': item.name,
                  'login': item.login,
                  'email': item.email} for item in users]
        }
    )


@blueprint.route('/api/teachers/<int:teacher_login>', methods=['GET'])
def get_one_users(teacher_login):
    db_sess = db_session.create_session()
    teacher = db_sess.query(Teacher).filter(teacher_login == Teacher.login).first()
    if not teacher:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'teacher':
                {'surname': teacher.surname,
                 'name': teacher.name,
                 'login': teacher.login,
                 'email': teacher.email}
        }
    )

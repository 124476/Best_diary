import flask
from flask import jsonify

from data import db_session
from data.tems import Tems

blueprint = flask.Blueprint(
    'tems_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/tems')
def get_tems():
    db_sess = db_session.create_session()
    tems = db_sess.query(Tems).all()
    if not tems:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'tems':
                [{'id': item.id,
                  'name': item.name,
                  'text': item.text} for item in tems]
        }
    )


@blueprint.route('/api/tems/<int:tem_id>', methods=['GET'])
def get_one_tem(tem_id):
    db_sess = db_session.create_session()
    tem = db_sess.query(Tems).filter(tem_id == Tems.id).first()
    if not tem:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user':
                {'id': tem.id,
                 'name': tem.name,
                 'text': tem.text}
        }
    )


@blueprint.route('/api/tems/delete/<int:tem_id>', methods=['GET'])
def delete_one_tem(tem_id):
    db_sess = db_session.create_session()
    tem = db_sess.query(Tems).filter(tem_id == Tems.id).first()
    if not tem:
        return jsonify({'error': 'Not found'})
    db_sess.delete(tem)
    db_sess.commit()
    return "Удалено!"

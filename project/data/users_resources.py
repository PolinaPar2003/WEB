from flask_restful import Resource, abort, reqparse
from flask import jsonify
from . import db_session
from .users import User

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'surname', 'email', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).filter(User.id == user_id).first()
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'name', 'surname', 'email', 'hashed_password')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User()
        users.id = args.json['id']
        users.name = args.json['name']
        users.surname = args.json['surname']
        users.email = args.json['email']
        users.hashed_password = args.json['hashed_password']
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})

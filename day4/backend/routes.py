from flask import request, jsonify, make_response
from flask_security import login_user
from flask_restful import Resource

from models import db, user_datastore

# @app.route('/signup', methods=['POST'])
# def signup():

class signup_fr(Resource):
    def post(self):
        data = request.get_json()
        if user_datastore.find_user(email=data['email']):
            return {'status': 'user already exists, use a different email'}
        if data['role'] == 'manager':
            role=['manager']
            active_status=False
        else:
            role=['customer']
            active_status=True
        user_datastore.create_user(
            name=data['name'],
            email=data['email'],
            password=data['password'],
            roles=role,
            active=active_status
        )
        db.session.commit()
        return {'status': 'user created'}

# @app.route('/signin', methods=['POST'])
# def signin():
class signin_fr(Resource):
    def post(self):
        data = request.get_json()
        user = user_datastore.find_user(email=data['email'])
        if user:
            if user.password == data['password']:
                if user.active:
                    login_user(user)
                    db.session.commit()
                    return {'status': 'login successful', 'authToken': user.get_auth_token()}
                return make_response(jsonify({'status': 'login failed, contact admin'}), 401)
            return make_response(jsonify({'status': 'login failed, incorrect password'}), 401)
        return make_response(jsonify({'status': 'login failed, user not found'}), 404)
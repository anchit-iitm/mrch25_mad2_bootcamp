from flask import Flask, render_template, request, redirect, url_for
from flask_security import Security, auth_required, roles_accepted, current_user, login_user
from flask_restful import Api
from flask_cors import CORS

from models import db, user_datastore
from config import development_config
from routes import signup_fr, signin_fr

app = Flask(__name__)
app.config.from_object(development_config)
CORS(app)

db.init_app(app)
Security(app, user_datastore)
api = Api(app)

api.add_resource(signup_fr, '/api/register')
api.add_resource(signin_fr, '/api/login')

@app.route('/signup', methods=['POST']) #/api/register
def signup():
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

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    user = user_datastore.find_user(email=data['email'])
    if user:
        if user.password == data['password']:
            if user.active:
                login_user(user)
                db.session.commit()
                return {'status': 'login successful', 'authToken': user.get_auth_token()}
            return {'status': 'login failed, contact admin'}
        return {'status': 'login failed, incorrect password'}
    return {'status': 'login failed, user not found'}


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/about')
@auth_required('token')
def about():
    return {'title': 'welcome to the about page', 'content': 'about about about'}

@app.route('/print', methods=['GET', 'POST'])
@auth_required('token')
def print_on_html():
    if request.method == 'POST':
        return {'name': request.json['name']}
    return {'instruction': 'use the post method to send the name, in a json format'}

@app.route('/print/<name>')
@auth_required('token')
def print_on_html2(name):
    return {'name': name, 'instruction': 'use the post method to send the name, in a json format'}

'''# @app.route('/store', methods=['POST'])
# def store():
#     new_data = user(name=request.json['name'])
#     db.session.add(new_data)
#     db.session.commit()
#     return {'status': 'data stored', 'id': new_data.id, 'name': new_data.name}
# 
# wont be working'''

@app.route('/users')
@auth_required('token')
@roles_accepted('admin')
def users():
    from models import user
    users = user.query.all()
    return {'users': [{'id': user.id, 'name': user.name} for user in users]}

@app.route('/user/<id>')
@auth_required('token')
@roles_accepted('admin')
def user(id):
    from models import user
    user = user.query.filter_by(id=id).first()
    return {'id': user.id, 'name': user.name}

@app.route('/details')
@auth_required('token')
def details():
    return {'email': current_user.email, 'name': current_user.name, 'roles': [role.name for role in current_user.roles], 'active': current_user.active}

if __name__ == '__main__':
    app.run()

# change to demostrate update through git
from flask import Flask, render_template, request, redirect, url_for
from flask_security import Security, auth_required, roles_accepted, current_user, login_user
from flask_restful import Api
from flask_cors import CORS
from celery import Celery
from celery.schedules import crontab

from models import db, user_datastore
from config import development_config
from routes import signup_fr, signin_fr, category, categories, product, products
from caching import cache
from mailing import mail

def create_celery(app):
    from config import celery_config
    celery_init = Celery(app.import_name)
    celery_init.config_from_object(celery_config)
    return celery_init

def create_app():
    app = Flask(__name__)
    app.config.from_object(development_config)
    CORS(app)

    db.init_app(app)
    Security(app, user_datastore)
    api = Api(app)
    mail.init_app(app)
    return app, api

app, api = create_app()

cache.init_app(app)

celery_app = create_celery(app)
celery_app.conf.beat_schedule = {
    'hello': {
        'task': 'tasks.send_mail',
        'schedule': crontab(minute=10, hour=21, day_of_month=27)
    }
}
import tasks

api.add_resource(signup_fr, '/api/register')
api.add_resource(signin_fr, '/api/login')
api.add_resource(category, '/api/category/<id>')
api.add_resource(categories, '/api/categories')
api.add_resource(product, '/api/product')
api.add_resource(products, '/api/products')

@app.route('/hello')
def hello_world():
    task = tasks.send_mail.delay()
    while not task.ready():
        pass
    print(task.result)
    return "True"

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
from flask import Flask, render_template, request, redirect, url_for

from models import db, User
from config import development_config

app = Flask(__name__)
app.config.from_object(development_config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/about')
def about():
    return {'title': 'welcome to the about page', 'content': 'about about about'}

@app.route('/print', methods=['GET', 'POST'])
def print_on_html():
    if request.method == 'POST':
        return {'name': request.json['name']}
    return {'instruction': 'use the post method to send the name, in a json format'}

@app.route('/print/<name>')
def print_on_html2(name):
    return {'name': name, 'instruction': 'use the post method to send the name, in a json format'}

@app.route('/store', methods=['POST'])
def store():
    new_data = User(name=request.json['name'])
    db.session.add(new_data)
    db.session.commit()
    return {'status': 'data stored', 'id': new_data.id, 'name': new_data.name}

@app.route('/users')
def users():
    users = User.query.all()
    return {'users': [{'id': user.id, 'name': user.name} for user in users]}

@app.route('/user/<id>')
def user(id):
    user = User.query.filter_by(id=id).first()
    return {'id': user.id, 'name': user.name}

if __name__ == '__main__':
    app.run()

# change to demostrate update through git
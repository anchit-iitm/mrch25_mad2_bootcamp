from app import celery_app
from models import category, user as user_model
from context import ContextTask
from mailing import mail

from flask_mail import Message


@celery_app.task(base=ContextTask)
def hello():
    return 'Hello, World!'

@celery_app.task(base=ContextTask)
def fetch_category(id):
    cat = category.query.filter_by(id=id).first_or_404()
    return cat.name

@celery_app.task(base=ContextTask)
def send_mail():
    users = user_model.query.all()
    for user in users:
        if user.roles[0].name == 'manager' or user.roles[0].name == 'customer':
            msg = Message(subject='Hello', recipients=[user.email], sender='dont_reply@a.com')
            msg.body = 'Hello, ' + user.name
            msg.html = '<b>Hello, ' + user.name + '</b>'
            mail.send(msg)
    return 'mail sent'


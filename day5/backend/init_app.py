from models import db, user_datastore
from app import app

with app.app_context():
    db.create_all()
    user_datastore.find_or_create_role(name='admin')
    user_datastore.find_or_create_role(name='manager')
    user_datastore.find_or_create_role(name='customer')

    if not user_datastore.find_user(email='admin@abc.com'):
        user_datastore.create_user(
            name='admin',
            email='admin@abc.com',
            password='admin',
            roles=['admin']
        )
    db.session.commit()
from flask import request, jsonify, make_response
from flask_security import login_user, auth_required, roles_accepted, current_user
from flask_restful import Resource

from models import db, user_datastore
from caching import cache

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
    
class category(Resource):
    @auth_required('token')
    def get(self, id):
        from models import category
        if id:
            categories = category.query.filter_by(id=id).first()
            if categories:
                return {'category': categories.name, 'description': categories.description, 'id': categories.id}
            return {'status': 'category not found'}
        return {'status': 'category id not provided'}

    @auth_required('token')
    @roles_accepted('admin', 'manager')    
    def put(self, id):
        from models import category
        data = request.get_json()
        if data:
            categories = category.query.filter_by(id=id).first()
            if categories:
                categories.name = data['name']
                categories.description = data['description']
                db.session.commit()
                return {'status': 'category updated', 'id': categories.id}
            return {'status': 'category not found'}
        return {'status': 'category id not provided'}
    
    def delete(self, id):
        from models import product
        if id:
            from models import category
            categories = category.query.filter_by(id=id).first()
            if categories:
                db.session.delete(categories)
                db.session.commit()
                return {'status': 'category deleted'}
            return {'status': 'category not found'}
    
class categories(Resource):
    @auth_required('token')
    @cache.cached(timeout=40)
    def get(self):
        from models import category
        categories = category.query.all()
        return {'categories': [{'id': i.id, 'name': i.name, 'description': i.description} for i in categories]}
    
    @auth_required('token')
    @roles_accepted('admin')
    def post(self):
        from models import category
        data = request.get_json()
        if data['name'] and data['description']:
            category = category(name=data['name'], description=data['description'])
            db.session.add(category)
            db.session.commit()
            return {'status': 'category created', 'id': category.id}
        return {'status': 'category name or description not provided'}
    
class product(Resource):
    @auth_required('token')
    def get(self):
        from models import product
        data = request.get_json()
        if data['id']:
            products = product.query.filter_by(id=data['id']).first()
            if products:
                return {'product': products.name, 'description': products.description, 'price': products.price, 'id': products.id, 'category_id': products.category_id}
            return {'status': 'product not found'}
        return {'status': 'product id not provided'}

    @auth_required('token')
    @roles_accepted('admin', 'manager')   
    def put(self):
        from models import product
        data = request.get_json()
        if data:
            products = product.query.filter_by(id=data['id']).first()
            if products:
                products.name = data['name']
                products.description = data['description']
                products.price = data['price']
                products.category_id = data['category_id']
                db.session.commit()
                return {'status': 'product updated', 'id': products.id}
            return {'status': 'product not found'}
        return {'status': 'product id not provided'}
    
class products(Resource):
    @auth_required('token')
    @cache.cached(timeout=40)
    def get(self):
        from models import product
        products = product.query.all()
        return {'products': [{'id': i.id, 'name': i.name, 'description': i.description, 'price': i.price, 'category_id': i.category_id} for i in products]}
    
    @auth_required('token')
    @roles_accepted('admin', 'manager')
    def post(self):
        from models import product
        data = request.get_json()
        if data['name'] and data['description'] and data['price'] and data['category_id']:
            product = product(name=data['name'], description=data['description'], price=data['price'], category_id=data['category_id'])
            db.session.add(product)
            db.session.commit()
            return {'status': 'product created', 'id': product.id}
        return {'status': 'product name, description or price not provided'}
    
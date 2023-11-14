#!/usr/bin/env python3
from models import Client, Store, GoodsService, Transaction
from flask import make_response, request
from config import db, bcrypt

# Local imports
from config import app, db

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

#---------------------------------------------------------------------------------------------------VIEW ALL CLIENTS [GET]-------------
@app.route('/clients', methods=['GET'])
def clients():
    clients = Client.query.all()
    resp = make_response([client.to_dict(rules=('-password_hash', '-transactions.stores.password_hash')) for client in clients], 200)
    return resp




#---------------------------------------------------------------------------------------------------VIEW ALL TRANSACTIONS [GET]-------------
@app.route('/transactions', methods=['GET'])
def transactions():
    transactions = Transaction.query.all()
    resp = make_response([transaction.to_dict(rules=('-clients.password_hash', '-stores.password_hash')) for transaction in transactions], 200)
    return resp


#---------------------------------------------------------------------------------------------------CREATE STORE [POST]-------------
@app.route('/create_store', methods=['POST'])
def create_store():
    form_data = request.get_json()
    new_store = Store(
        name=form_data['name'],
        email=form_data['email'],
    )
    hashed_password = bcrypt.generate_password_hash(form_data['password']).decode('utf-8')
    new_store.password_hash = hashed_password
    db.session.add(new_store)
    db.session.commit()
    resp = make_response(new_store.to_dict(), 201)
    
    return resp

#---------------------------------------------------------------------------------------------------CREATE NEW GOODS/SERVICE [POST]-------------
@app.route('/create_goods_service', methods=['POST'])
def create_goods_service():
    form_data = request.get_json()
    new_goods_service = GoodsService(
        name=form_data['name'],
        price=form_data['price'],
    )
    db.session.add(new_goods_service)
    db.session.commit()
    resp = make_response(new_goods_service.to_dict(), 201)
    return resp

#---------------------------------------------------------------------------------------------------CREATE NEW CLIENT [POST]-------------
@app.route('/create_client', methods=['POST'])
def create_client():
    form_data = request.get_json()
    new_client = Client(
        name=form_data['name'],
        email=form_data['email'],
    )
    hashed_password = bcrypt.generate_password_hash(form_data['password']).decode('utf-8')
    new_client.password_hash = hashed_password # Hash the password with bcrypt
    db.session.add(new_client)
    db.session.commit()

    resp = make_response(new_client.to_dict(), 201)
    return resp


#---------------------------------------------------------------------------------------------------CREATE TRANSACTION [POST]-------------
@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    form_data = request.get_json()
    new_transaction = Transaction(
        total_amount=form_data['total_amount'],
        store_id=form_data['store_id'],
        client_id=form_data['client_id'],
    )
    db.session.add(new_transaction)
    db.session.commit()

    resp = make_response(new_transaction.to_dict(), 201)
    return resp







if __name__ == '__main__':
    app.run(port=5555, debug=True)







# @app.route('/')
# def index():
#     return '<h1>Project Server</h1>'



# #-----------------CREATE_USER--------------------------
# @app.route('/create_user', methods=['POST'])
# def create_user():
#     form_data = request.get_json()
#     new_user = User(
#         username=form_data['username'],
#         email=form_data['email'],
#         is_store=form_data['is_store']
#         )
#     hashed_password = bcrypt.generate_password_hash(form_data['password']).decode('utf-8')
#     new_user.password_hash = hashed_password
#     db.session.add(new_user)
#     db.session.commit()
#     return make_response({'message': 'User created successfully'}, 201)


# #-----------------CREATE_GOODS_SERVICE--------------------------
# @app.route('/create_goods_service', methods=['POST'])
# def create_goods_service():
#     form_data = request.get_json()
#     new_goods_service = GoodsService(
#         name=form_data['name'],
#         price=form_data['price'],
#         store_id=form_data['store_id']
#         )
#     db.session.add(new_goods_service)
#     db.session.commit()
#     return make_response({}, 201)


# #-----------------VIEW_TRANSACTIONS--------------------------
# @app.route('/view_transactions/<int:user_id>', methods=['GET'])
# def view_transactions(user_id):
#     user = User.query.filter_by(id == user_id).first()
#     if user:
#         if request.method == 'GET':
#             transactions = user.transactions
#             resp = [transaction.to_dict(rules='', ) for transaction in transactions]
#             return make_response(resp, 200)
#     else:
#         resp = make_response({ "errors": "No Transactions Found!"}, 404)
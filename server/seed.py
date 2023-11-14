#!/usr/bin/env python3

from models import Client, Store, GoodsService, Transaction
# Remote library imports

# Local imports
from app import app
from config import db, bcrypt


with app.app_context():
    print("Starting seed...")
    # Seed code goes here!

    Client.query.delete()
    Store.query.delete()
    GoodsService.query.delete()
    Transaction.query.delete()

    new_client = Client(
        id=1,
        name="Joseph Smith", 
        email="Joe@youmail.com", 
        password_hash='hashed_password'
        )

    new_store = Store(
        id = 1,
        name="CarWashers", 
        email="CarWashers@business.com",
        password_hash='hashed_password' 
        )
    
    new_goods_service = GoodsService(
        name = "Full Wash - Inside/Out",
        price = 60,
        store_id = 1
    )

    new_transaction = Transaction(
        total_amount=32.50,
        store_id=1,
        client_id=1
    )

    # Adding the client to the session
    db.session.add(new_client)
    db.session.add(new_store)
    db.session.add(new_goods_service)
    db.session.add(new_transaction)

    # Committing the changes to the database
    db.session.commit()
    print('Done with seeding...')
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
# from enum import Enum, auto

from config import db, bcrypt
# import re


#---------------------------------------------------------------------
#-----------------------CLASS Store-----------------------
class Store(db.Model, SerializerMixin):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)



    # One-to-Many relationship with GoodsService
    goods_services = db.relationship('GoodsService', back_populates='stores', lazy=True)

    # One-to-Many relationship with Transaction
    transactions = db.relationship('Transaction', back_populates='stores', lazy=True)


    serialize_rules = ('-goods_services.stores', '-transactions.stores')


    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check if the provided password matches the hashed password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    

    # Validation: Ensure email is not empty and has a valid format
    @validates('email')
    def validates_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError("Invalid email format")
        return email


#--------------------------------------------------------------------------------------------    
#----------------- CLASS GoodsService -----------------------
class GoodsService(db.Model, SerializerMixin):
    __tablename__ = 'goods_services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    # Many-to-Many relationship with Store
    stores = db.relationship('Store', back_populates='goods_services', lazy=True)

    serialize_rules = ('-stores.goods_services', )


#--------------------------------------------------------------------------------------------
#----------------- CLASS Client -----------------------
class Client(db.Model, SerializerMixin):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    
    # One-to-Many relationship with Transaction
    transactions = db.relationship('Transaction', back_populates='clients', lazy=True)

    serialize_rules = ('-transactions.clients', )

    # Set the password using bcrypt
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check if the provided password matches the hashed password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Validation: Ensure email is not empty and has a valid format
    @validates('email')
    def validates_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError("Invalid email format")
        return email

#---------------------------------------------------------------------
#----------------- CLASS Transaction -----------------------
class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    # Foreign keys
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    # Relationships
    stores = db.relationship('Store', back_populates='transactions', lazy=True)
    clients = db.relationship('Client', back_populates='transactions', lazy=True)

    serialize_rules = ('-stores.transactions', '-clients.transactions')












# #----------------------------------CLASS User-------------------------------
# class User(db.Model, SerializerMixin):
#     __tablename__='users'
#     id = db.Column(db.Integer, primary_key=True)
#     profile_photo = db.Column(db.String())
#     username = db.Column(db.String(), unique=True, nullable=False, unique=True)
#     email = db.Column(db.String(), unique=True, nullable=False, unique=True)
#     password_hash = db.Column(db.String(), nullable=False, unique=True)
#     is_store = db.Column(db.Boolean, default=False)  # Identify if the user is a store
    
#     goods_services = db.relationship('GoodsService',  secondary=user_goods_service_association, back_populates='store', lazy=True)
    
#     transactions = db.relationship('Transaction', back_populates='client', lazy=True)
#     notifications = db.relationship('Notification', back_populates='client', lazy=True)

# #-------------SERIALIZE RULES-------------------------------
#     serialize_rules = ('-goods_services.user', '-transactions.client', '-notifications.client')

#     # Set the password using bcrypt
#     def set_password(self, password):
#         self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

#     # Check if the provided password matches the hashed password
#     def check_password(self, password):
#         return bcrypt.check_password_hash(self.password_hash, password)

# #------------------------VALIDATIONS FOR USER------------------------
#     @validates('username')
#     def validates_username(self, key, username):
#         if not username:
#             raise ValueError("Username cannot be empty")

#     # Validation: Ensure email is not empty and has a valid format
#     @validates('email')
#     def validates_email(self, key, email):
#         if not email or '@' not in email:
#             raise ValueError("Invalid email format")
#         return email

#     def __repr__(self):
#         return f''




# #----------------- SUBCLASSES FOR USER-----------------------
# class Store(User):
#     __tablename__ = 'stores'
#     id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

#     def __repr__(self):
#         return f''


# class Customer(User):
#     __tablename__ = 'customers'
#     id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

#     def __repr__(self):
#         return f''






# #----------------------------------CLASS GoodsService-------------------------------
# class GoodsService(db.Model, SerializerMixin):
#     __tablename__='goods_services'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(), nullable=False)
#     price = db.Column(db.Float, nullable=False)

#     store_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

#     @validates('name')
#     def validates_name(self, key, name):
#         if not name:
#             raise ValueError("Name cannot be empty")

# #-------------SERIALIZE RULES-------------------------------
#     serialize_rules = ('-store.goods_services', '-store.transactions', '-store.notifications')

#     def __repr__(self):
#         return f''


# #----------------------------------CLASS Transaction-------------------------------
# class Transaction(db.Model, SerializerMixin):
#     __tablename__='transactions'
#     id = db.Column(db.Integer, primary_key=True)
#     client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     total_amount = db.Column(db.Float, nullable=False)
#     timestamp = db.Column(db.DateTime, default=db.func.now())

# #-------------SERIALIZE RULES-------------------------------
#     serialize_rules = ('-client.goods_services', '-client.transactions', '-client.notifications')

#     def __repr__(self):
#         return f''


# #----------------------------------CLASS Notification-------------------------------
# class FrequencyDays(Enum):
#     EVERY_15_DAYS = auto()
#     EVERY_30_DAYS = auto()
    
# # how IM going to call this function:  new_notification = Notification(message="Your message", frequency_days=FrequencyDays.EVERY_15_DAYS)



# class Notification(db.Model, SerializerMixin):
#     __tablename__='notifications'
#     id = db.Column(db.Integer, primary_key=True)
#     client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     message = db.Column(db.Text, nullable=False)
#     frequency_days = db.Column(db.Integer, nullable=False)
#     last_sent = db.Column(db.DateTime, default=db.func.now())

# #-------------SERIALIZE RULES-------------------------------
#     serialize_rules = ('-client.goods_services', '-client.transactions', '-client.notifications')

#     def __repr__(self):
#         return f''

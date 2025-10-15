from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

db = SQLAlchemy()

class BaseClass(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=func.now())  # Use utcnow for better practice
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


class Users(BaseClass):
    __tablename__ = 'users'  # Explicitly defining the table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)  # Ensure username is unique
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    balance = db.Column(db.Integer, default=0)  # Initialize balance to 0
    role_id = db.Column(db.Integer, default=1)  # Default role ID

class Products(BaseClass):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False, unique=True)  
    category = db.Column(db.String(20))
    price = db.Column(db.Float, nullable=False) 
    availability = db.Column(db.Integer, nullable=False,default=1)
    quantity = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    ratings = db.Column(db.Float)

class Tokens(db.Model):
    __tablename__ = 'tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to Users
    token = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expired_at = db.Column(db.DateTime, nullable=False)

class CartPurchase(BaseClass):
    __tablename__ = 'cart_purchases'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to Users
    status = db.Column(db.String(15), nullable=False)
    purchase_code = db.Column(db.String(10), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)  # Foreign key to Products

class Purchase(BaseClass):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to Users
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Foreign key to Products
    status = db.Column(db.String(15))
    ordered_on = db.Column(db.DateTime)
    shipped_on = db.Column(db.DateTime)
    delivered_on = db.Column(db.DateTime)
    purchase_code = db.Column(db.String(10))
    quantity = db.Column(db.Integer)

class UserHistory(db.Model):
    __tablename__ = 'user_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to Users
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))  # Foreign key to Products
    times_searched = db.Column(db.Integer, default=0)  # Initialize to 0
    is_favorite = db.Column(db.Integer, default=False)  # Changed to Boolean for clarity

class Coupons(db.Model):
    __tablename__ = 'coupons'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)  # Ensure coupon code is unique
    discount = db.Column(db.Float, nullable=False)  # Use Float for discounts
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    valid_till = db.Column(db.DateTime, nullable=False)

class Permissions(BaseClass):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)  # Assuming you have a roles table
    method = db.Column(db.String(10), nullable=False)  # Specify method (GET, POST, etc.)
    endpoint = db.Column(db.String(100), nullable=False)  # Specify endpoint
    status = db.Column(db.Boolean, default=True)  # Use Boolean for active/inactive status



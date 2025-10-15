from flask_restful import Resource
from flask import request,jsonify
import jwt
import re
from datetime import datetime
from flasgger import swag_from
from helper import create_specs_from_schema_user,validateswaggerinput,SECRET_KEY,DB_CONFIG
from schemas import SignupSchema
from models import Users,db

def is_valid_password(password="", username=""):
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!_#%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    if not(username and password):
        raise ValueError(101)
    if not re.match(password_regex, password):
        raise ValueError(109)

def check_user_exist(email, username):
    user_exists = Users.query.filter_by(username=username).first()
    if user_exists:
        raise ValueError(105)
    email_exist = Users.query.filter_by(email=email).first()
    if email_exist:
        raise ValueError(106)

def get_credentials(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    address = data.get('address')
    return username, email, password,address

def insert_into_database(username, password, email,address):
    password = jwt.encode({"password": password}, SECRET_KEY, algorithm="HS256")
    new_user = Users(username=username,email=email,password=password,address=address,role_id=1)
    db.session.add(new_user)
    db.session.commit()
            

class Signup(Resource):
    specs_dict = create_specs_from_schema_user(SignupSchema, summary="Signing up a new user", tag="User", method="post")
    @swag_from(specs_dict)
    def post(self):
        data = request.get_json()
        username, email, password,address = get_credentials(data)
        validateerror = validateswaggerinput(SignupSchema, data)
        if validateerror:
            return validateerror
        is_valid_password(username=username, password=password)
        check_user_exist(email=email, username=username) 
        insert_into_database(email=email, username=username, password=password,address=address)
        return jsonify({"errorCode": 0, "errorMessage" : "Successfully Registered"})  

    

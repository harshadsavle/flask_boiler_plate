from flask_restful import Resource
from flask import request,jsonify,g
import jwt
from flasgger import swag_from
from helper import create_specs_from_schema_user, validateswaggerinput,SECRET_KEY,DB_CONFIG,AUTH_KEY
from schemas import LoginSchema
from datetime import datetime, timedelta
from models import Users,Tokens,db
from timeit import default_timer as timer

def getcredentials(data):
    username = data.get('username')
    password = data.get('password')
    return username, password

def insert_token_into_db(token,user_id):
    created_at = datetime.now()
    expired_at = created_at + timedelta(hours=2)
    token_in_db = Tokens.query.filter_by(user_id=user_id).first()
    if not token_in_db:
        token = Tokens(
            token = token,
            user_id = user_id,
            created_at = created_at,
            expired_at = expired_at
        )
        db.session.add(token)
    else:    
        token_in_db.token = token
        token_in_db.created_at = created_at
        token_in_db.expired_at = expired_at
    db.session.commit()

class Login(Resource):
    specs_dict = create_specs_from_schema_user(LoginSchema, summary="Logging in the user", tag="User", method="get")
    @swag_from(specs_dict)
    def get(self):
        data = request.args 
        username, password = getcredentials(data)
        validateresult = validateswaggerinput(LoginSchema,data)
        time = datetime.now()
        time = str(time)
        if validateresult:
            return validateresult
        if not (username and password):
            raise ValueError(101)   
        current_user = Users.query.filter_by(username=username).first()
        password_token = jwt.encode({"password": password}, SECRET_KEY, algorithm="HS256")
        auth_token = jwt.encode({"username": username, "password": password}, AUTH_KEY, algorithm="HS256",)
        jwt.decode(auth_token,AUTH_KEY,algorithms="HS256")
        if not current_user:
            raise ValueError(108)
        if current_user.password!=password_token:
            raise ValueError(107)
        user_id = current_user.id
        insert_token_into_db(auth_token,user_id)
        return jsonify({"errorCode":0, "errorMessage": "Login successful!", "token":auth_token})


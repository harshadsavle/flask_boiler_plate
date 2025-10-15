from flask_restful import Resource
from flask import request,jsonify
import jwt
import re
from flasgger import swag_from
from helper import create_specs_from_schema_user, validateswaggerinput,SECRET_KEY,DB_CONFIG,token_required
from schemas import ChangeSchema
from models import Users,db
from datetime import datetime

def is_valid_password_username_secretkey(oldpassword="", newpassword=""):
    password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    
    if not(oldpassword and newpassword):
        raise ValueError(101)
    if not re.match(password_regex, newpassword):
        raise ValueError(109)

def getcredentials(data):
    oldpassword = data.get('oldpassword')
    newpassword = data.get('newpassword')
    return oldpassword,newpassword

class ChangePassword(Resource):
    specs_dict = create_specs_from_schema_user(ChangeSchema, summary="Changing the password of a user", tag="User", method="put")
    @swag_from(specs_dict)
    @token_required
    
    def put(self,**kwargs):
        user_id = kwargs.get('user_id')
        data = request.form
        oldpassword,newpassword = getcredentials(data)
        validateresult = validateswaggerinput(ChangeSchema,data)
        if validateresult:
            return validateresult
        if not (oldpassword and newpassword):
            raise ValueError(101)
        is_valid_password_username_secretkey(oldpassword=oldpassword,newpassword=newpassword)
        newpassword = jwt.encode({"password" : newpassword}, SECRET_KEY, algorithm='HS256')
        password_in_db = Users.query.filter_by(id=user_id).first().password
        password_in_db = jwt.decode(password_in_db,SECRET_KEY,"HS256").get('password')
        result = Users.query.filter_by(id=user_id).first()
        if password_in_db!=oldpassword:
            raise ValueError(119)
        if not result:
            raise ValueError(108)
        result.password = newpassword
        db.session.commit()
        return jsonify({'errorCode' : 0, 'errorMessage':'Password changes successfully'})





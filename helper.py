from marshmallow import ValidationError 
from flask import jsonify,request
from dotenv import load_dotenv
import os
from functools import wraps
from models import Tokens,Users,Permissions
from datetime import datetime
import re

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
AUTH_KEY = os.getenv('AUTH_KEY')
DB_CONFIG = {
    "host": os.getenv('DB_HOST'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "database": os.getenv('DB_DATABASE')
}

def remove_last_integer_from_url(url):
    updated_url = re.sub(r'/\d+$', '/', url)
    return updated_url

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "Authorization" not in request.headers:
            raise ValueError(121)
        token = request.headers.get('Authorization').split(" ")[1]
        token_in_db = Tokens.query.filter_by(token = token).first()
        # here i am not decoding because it is better to check with db, say if admin removed this token to prevent entry of a user, here it will stop him
        # but if i simply decode the token and move forward, then it will be able to access even if he is not allowed
        if not token_in_db:
            raise ValueError(123)
        expired_at = token_in_db.expired_at
        if datetime.now()>expired_at:
            raise ValueError(120)
        user_id = token_in_db.user_id
        user = Users.query.filter_by(id=user_id).first()
        role_id = user.role_id
        # path = remove_last_integer_from_url(request.path)
        # permission_obj = Permissions.query.filter_by(role_id=role_id,method=request.method,endpoint=path).first()
        # if not permission_obj:
        #     raise ValueError(130)
        return f(*args, user_id=user_id,role=role_id, **kwargs)

    return decorated





def create_specs_from_schema_user(schema,summary,tag,method,tokenrequired=False):
    parameters = {}
    auth_parameter = {
                'name': "Authorization",
                'in': 'header',
                'required': True,
                'schema' : {
                    'type': 'string',
                    'example' : 'Bearer XXXX'
                }
            }
    
    for field_name, field in schema().fields.items():
        field_type = type(field).__name__.replace('Field', '').lower()
        parameters[field_name] = {'type': field_type}

    if method.upper() == 'POST':

        query_parameters = []
        body_schema = {
            'type': 'object',
            'properties': {}
        }

        for field_name, field_info in parameters.items():
            body_schema['properties'][field_name] = {'type': field_info['type']}

        query_parameters.append({
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': body_schema
        })

    elif method.upper()=="PUT":
        query_parameters = []
        for field_name, field_info in parameters.items():
            query_parameters.append({
                'name': field_name,
                'in': 'formData',
                'required': False,
                'type': field_info['type']
            }),
        query_parameters.append(auth_parameter),
    else:
        query_parameters = []
        for field_name, field_info in parameters.items():
            query_parameters.append({
                'name': field_name,
                'in': 'query',
                'required': False,
                'type': field_info['type'],
            }),
        if tokenrequired:
            query_parameters.append(auth_parameter)
    specs_dict = {
        'summary': summary,
        'parameters': query_parameters,
        'tags': [tag],
        'responses': {
            '200': {
                'description': 'Request Successful'
            }
        },
        'route': 'apidocs',
    }
    

    return specs_dict


def create_specs_from_schema_product(schema, summary, tag, parametertype="formData", requires_file=False, method="GET"):
    parameters = {}
    auth_parameter = {
                'name': "Authorization",
                'in': 'header',
                'required': True,
                'schema' : {
                    'type': 'string',
                    'example' : 'Bearer <yout-jwt-token>'
                }
            }
    for field_name, field in schema().fields.items():
        field_type = type(field).__name__.replace('Field', '').lower()
        parameters[field_name] = {'type': field_type}
    query_parameters = []
    if method!="POST":
        query_parameters.append({
                'name': "product_id",
                'in': 'path',
                'required': False,
                'type': 'integer'
            }
            )
    for field_name, field_info in parameters.items():
        if field_name!="id":
            query_parameters.append({
                'name': field_name,
                'in': parametertype,
                'required': False,
                'type': field_info['type']
            })
    query_parameters.append(auth_parameter),
    if requires_file:
        query_parameters.append({
            'in': 'formData',
            'name': 'file',
            'type': 'file',
            'required': False,
            'description': 'Upload an image for the product'
        })

    specs_dict = {
        'summary': summary,
        'parameters': query_parameters,
        'tags': [tag],
        'responses': {
            '200': {
                'description': 'Request Successful'
            }
        },
        'route': 'apidocs',
        'security': [{
        "Bearer": []
    }]
    }
    
    return specs_dict




def validateswaggerinput(schema_class,data):
        try:
            schema = schema_class()
            schema.load(data)
        except ValidationError as err:
            return jsonify({"errorCode": 400, "errorMessage": err.messages})
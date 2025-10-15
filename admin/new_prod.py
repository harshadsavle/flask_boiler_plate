from flask_restful import Resource
from flask import request,jsonify
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from datetime import datetime
from helper import create_specs_from_schema_product, validateswaggerinput,DB_CONFIG,token_required
from schemas import NewProdSchema
from schemas import UpdateProdSchema
from flasgger import swag_from
from models import Products,db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



def check_product_exist(name):
    result = Products.query.filter_by(name=name).first()
    if result:
        raise ValueError(114)

def getvalues(data):
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')
    category = data.get('category')
    return name,price,quantity,category

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class NewProd(Resource):

    specs_dict = create_specs_from_schema_product(NewProdSchema, summary="Adding a new product to the database", tag="Product",requires_file=True, method="POST")
    @swag_from(specs_dict)
    @token_required
    def post(self,**kwargs):
        user_id =  kwargs.get('user_id')
        data = request.form
        name,price,quantity,category = getvalues(data)
        image = request.files.get('file')
        owner = user_id
        data = {'name': name, 'price': price, 'quantity': quantity, 'category':category}
        validateerror = validateswaggerinput(NewProdSchema,data)
        if validateerror:
            return validateerror
        if not (name and price and quantity):
            raise ValueError(101)
        check_product_exist(name)
        if not (image or allowed_file(image.filename)):
            raise ValueError(132)
        filename = secure_filename(image.filename)  
        image_path = os.path.join(os.getenv('UPLOAD_FOLDER'), filename)
        image.save(image_path)  
        image_url = f"{image_path}"
        product = Products(
            name = name,
            price  = price,
            quantity  = quantity,
            availability  = 1,
            image= image_url,
            owner_id= owner,
            category = category,
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"errorCode": 0, "errorMessage" : "Product successfully added"})  

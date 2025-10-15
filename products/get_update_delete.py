from flask_restful import Resource
from flask import request,jsonify
from datetime import datetime
from helper import create_specs_from_schema_product,validateswaggerinput,DB_CONFIG,token_required
from flasgger import swag_from
from models import Products,db,UserHistory    
from schemas import UpdateProdSchema,DeleteProdSchema,GetProdSchema



def check_product_exist(id_prod,user_id):
    result = Products.query.filter_by(id=id_prod,availability=1).first()
    if not (result):
        raise ValueError(111)
    if int(result.owner_id) != user_id:
        raise ValueError(131)
    
def get_credentials(data,id_prod):
    user = Products.query.filter_by(id=id_prod).first()
    price = data.get("price", user.price)
    quantity = data.get("quantity", user.quantity)
    return price,quantity

def add_to_user_history(product_id,user_id):
    product_exist = UserHistory.query.filter_by(product_id = product_id).first()
    if product_exist:
        product_exist.times_searched = int(product_exist.times_searched)+1
    else:
        new_entry = UserHistory(
            user_id = user_id,
            product_id = product_id,
            times_searched = 1,
            is_favorite = 0,
        )
        db.session.add(new_entry)
    db.session.commit()

class GetDeleteUpdateProd(Resource):

    specs_dict = create_specs_from_schema_product(DeleteProdSchema, summary="Completely removing a product from the database", tag="Admin")
    @swag_from(specs_dict)
    @token_required
    def delete(self,product_id=None,**kwargs):
        current_user = kwargs.get('user_id')
        id_prod = product_id
        if not id:
            raise ValueError(101)
        product = Products.query.filter_by(id=id_prod,availability=1).first()
        check_product_exist(id_prod,current_user)
        product.availability = 0
        product.updated_at = datetime.now()
        db.session.commit()
        return jsonify({"errorCode":0, "errorMessage":f"Product marked as inactive by {current_user}"})


    specs_dict = create_specs_from_schema_product(UpdateProdSchema, summary="Updating the details of a particular product", tag="Admin", requires_file=True)
    @swag_from(specs_dict)
    @token_required
    def put(self,product_id=None,**kwargs):
        user_id = kwargs.get('user_id')   
        data = request.form 
        check_product_exist(product_id,user_id)
        price,quantity = get_credentials(data,product_id)
        if not (product_id):
            raise ValueError(101)
        updated_at = datetime.now()
        product = Products.query.filter_by(id=product_id).first()
        product.price = price
        product.quantity = quantity
        product.updated_at = updated_at
        db.session.commit()
        return jsonify({"errorCode": 0, "errorMessage" : f"Details for product : {product_id} successfully updated by {user_id}"})  


    specs_dict = create_specs_from_schema_product(GetProdSchema, summary="Getting details about a particular product or the list of all items", tag="Product", parametertype="GET")
    @token_required
    @swag_from(specs_dict)

    def get(self, product_id=None, **kwargs):
        user_id = kwargs.get('user_id')
        product = Products.query.filter_by(id=product_id, availability=1).first() if product_id else Products.query.all()
        if product_id and not product:
           raise ValueError(118)
        if product_id:
           add_to_user_history(product.id, user_id)
        product = [product]
        dict_items = []
        for product in product:
            dict_items.append({
                "id":product.id,
                "name":product.name,
                "image_url" : product.image,
                "price": product.price,
                "availability" : product.availability,
                "quantity" : product.quantity,
                "updated_at" : product.updated_at,
                "owner_id" : product.owner_id
            })
        return jsonify({"items":dict_items})



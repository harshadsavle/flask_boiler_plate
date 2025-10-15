from flask_restful import Resource
import requests
from flask import request,jsonify
from helper import create_specs_from_schema_product,token_required
from schemas import AddToCartSchema
from flasgger import swag_from
from models import Products,CartPurchase,Users,db
from datetime import datetime


def check_product_exist(id_prod):
    result = Products.query.filter_by(id=id_prod,availability=1).first()
    if not (result):
        raise ValueError(111)

class AddToCart(Resource):

    specs_dict = create_specs_from_schema_product(AddToCartSchema, summary="Add a product to the cart to buy later", tag="Purchase")
    @swag_from(specs_dict)
    @token_required
    def post(self,product_id=None,**kwargs):

        base_url = f"{request.scheme}://{request.host}"
        product_url = f"{base_url}/product/{product_id}"
        token = request.headers.get('Authorization')
        user_id = kwargs.get('user_id')
        username = Users.query.filter_by(id=user_id).first().username
        check_product_exist(product_id)
        prod_exist_in_cart = CartPurchase.query.filter_by(user_id=user_id, product_id=product_id, status="cart").first()
        if not prod_exist_in_cart:
            product = CartPurchase(
                user_id = user_id,
                status = "cart",
                quantity  = 1,
                product_id = product_id,
                created_at = datetime.now()
            )
            db.session.add(product)
        db.session.commit()
        response = requests.get(product_url, headers={'Authorization' : token})
        return jsonify({"errorCode": 0,
                        "product_details" : str(response.json()),
                         "errorMessage" : f"{username} requested to add this product to cart : {product_id}"})  

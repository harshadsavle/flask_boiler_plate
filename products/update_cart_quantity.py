from flask_restful import Resource
from flask import request,jsonify
from helper import create_specs_from_schema_product,validateswaggerinput,DB_CONFIG,token_required
from flasgger import swag_from
from schemas import UpdateCartProductSchema
from models import CartPurchase,db

class UpdateCartProduct(Resource):
    specs_dict = create_specs_from_schema_product(UpdateCartProductSchema, summary="Updating the details of a particular product in a user's cart", tag="Admin", requires_file=False)
    @swag_from(specs_dict)
    @token_required
    def put(self,**kwargs):
        user_id = kwargs.get('user_id')
        details = request.form
        product_id = details.get('product_id')
        product_in_cart = CartPurchase.query.filter_by(user_id=user_id, product_id=product_id).first()
        remove = int(details.get('remove'))

        if product_in_cart is None:
            raise ValueError(118)
        if remove:
            db.session.delete(product_in_cart)
        else:
            product_in_cart.quantity = details.get('quantity')
        db.session.commit()
        return jsonify({"errorCode": 0, "errorMessage" : f"Details for product : {product_id} successfully updated by {user_id}"})  
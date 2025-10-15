from flask import request
from flask_restful import Resource
from models import Users,CartPurchase,Purchase,Products,db
from helper import create_specs_from_schema_user,token_required
from schemas import ProfileSchema
from flasgger import swag_from


class Profile(Resource):
    specs_dict = create_specs_from_schema_user(ProfileSchema, summary="Getting all personal info of a user", tag="User",method="get",tokenrequired=True)
    @swag_from(specs_dict)
    @token_required
    def get(self,**kwargs):

        user_id = kwargs.get('user_id')
        user_id = int(user_id)  
        user = Users.query.filter_by(id=user_id).first()
        cart = CartPurchase.query.filter_by(user_id=user_id,status="cart")
        if not user:
            raise ValueError(108)
        purchase_list = []
        cart_items = db.session.query(CartPurchase).join(Products).filter(CartPurchase.user_id == user_id,CartPurchase.status == "cart").with_entities(Products.id, Products.name, CartPurchase.quantity, Products.image, Products.price)
        purchases = db.session.query(Purchase).join(Products).filter(Purchase.user_id == user_id).with_entities(Products.id,
        Products.name, Products.price, Products.image, Purchase.ordered_on, Purchase.delivered_on
    ).all()
        purchase_dict = {}
        cart_dict = {}
        total_price = 0
        for item in purchases:
            purchase_object = {
                "id" : item[0],
                "name" : item[1],
                "price" : item[2],
                "image" : item[3],
                "purchased_on" : item[4],
                "delivered_on" : item[5]

            }
            purchase_dict[item[0]]= purchase_object
        for item in cart_items:
            quantity = item[2]
            price = item[4]
            price_current = quantity * price
            cart_object = {
                "id" : item[0],
                "name" : item[1],
                "quantity" : quantity,
                "image" : item[3],
                "price": price,
            }
            total_price +=price_current
            cart_dict[item[0]]=cart_object
        details = {
            "name" : user.username,
            "address" : user.address,
            "email" : user.email,
            "balance" : user.balance,
            "products_in_cart" : list(cart_dict.values()),
            "total_price" : total_price,
            "purchased_products" : list(purchase_dict.values()),
        }
        
        return {"errorCode":0, "details":str(details)}
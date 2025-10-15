from flask import jsonify,request
from flask_restful import Resource
from helper import token_required
import stripe

class Server(Resource):
    @token_required
    def post(self):
        stripe.api_key = "dummy api key start with sk"
        items = [{"unit_amount" : "20000","product_id":45 },
                {"unit_amount" : "3000","product_id":46 },
                {"unit_amount" : "780","product_id":47 },
                {"unit_amount" : "57000","product_id":48 },
                {"unit_amount" : "13000","product_id":49 }
                 ]
        stripe.Price.create(currency="inr",unit_amount=1000,product='{{PRODUCT_ID}}',)


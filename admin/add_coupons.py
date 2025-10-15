from helper import create_specs_from_schema_product,token_required
from models import db,Coupons
from schemas import AddCouponsSchema
from flasgger import swag_from
from flask import request,jsonify
from flask_restful import Resource
from datetime import datetime,timedelta



class AddCoupons(Resource):
    specs_dict = create_specs_from_schema_product(AddCouponsSchema, summary="Adding a new discount coupon", tag="Admin", method="put")
    @swag_from(specs_dict)
    @token_required
    def post(self,**kwargs):
        role = kwargs.get('role')
        if role!="admin":
            raise ValueError(126)
        data = request.form
        discount = data.get("discount")
        code = data.get("code")
        created_at = datetime.now()
        valid_till = created_at + timedelta(hours=48)
        coupon_exist = Coupons.query.filter_by(code=code).first()
        if coupon_exist:
            raise ValueError(128)
        coupon = Coupons(
            code=code,
            created_at = created_at,
            valid_till = valid_till,
            discount = discount
        )
        db.session.add(coupon)
        db.session.commit()
        return jsonify({"errorCode": 0, "errorMessage" : "Coupon added"})  

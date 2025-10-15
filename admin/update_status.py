from flask import request,jsonify
from flask_restful import Resource
from helper import create_specs_from_schema_user,token_required,validateswaggerinput
from flasgger import swag_from
from schemas import UpdateStatusSchema
from models import db,Products,Users,Purchase
from datetime import datetime

def get_credentials(data):
    id_purchase = data.get("id_purchase")
    purchase = Purchase.query.filter_by(id=id_purchase).first()
    status = data.get("status", purchase.status)
    shipped_on = data.get("shipped_on", purchase.shipped_on)
    delivered_on = data.get("delivered_on", purchase.delivered_on)
    return id_purchase,status,shipped_on,delivered_on

def check_purchase_exist(id_prod):
    result = Purchase.query.filter_by(id=id_prod).first()
    if not (result):
        raise ValueError(111)
    
class UpdateStatus(Resource):
    specs_dict = create_specs_from_schema_user(UpdateStatusSchema, summary="Updating the status of a particular purchase", tag="Admin", method="put")
    @swag_from(specs_dict)
    @token_required
    def put(self,**kwargs):
        current_user = kwargs.get('current_user')
        role = kwargs.get('role')
        if role!="admin":
            raise ValueError(126)
        data = request.form
        validateresult = validateswaggerinput(UpdateStatusSchema,data)
        if validateresult:
            return validateresult
        id_purchase,status,shipped_on,delivered_on = get_credentials(data)
        if not (id_purchase):
            raise ValueError(101)
        check_purchase_exist(id_prod=id_purchase)
        purchase = Purchase.query.filter_by(id=id_purchase).first()
        purchase.status = status
        purchase.shipped_on = shipped_on
        purchase.delivered_on = delivered_on
        purchase.updated_at = datetime.now()
        db.session.commit()
        return jsonify({"errorCode": 0, "errorMessage" : f"Details for purchase : {id_purchase} successfully updated by {current_user}"})  

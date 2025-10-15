from flask_restful import Resource
from flask import request,jsonify
from flasgger import swag_from
from helper import create_specs_from_schema_product,validateswaggerinput,DB_CONFIG,token_required
from models import Products,db,Users
from schemas import DeleteProdSchema

class DeleteProd(Resource):
    specs_dict = create_specs_from_schema_product(DeleteProdSchema, summary="Completely removing a product from the database", tag="Product", method="delete")
    @swag_from(specs_dict)
    @token_required
    def delete(self,id=None,**kwargs):
        user_id = kwargs.get('current_user')
        current_user = Users.query.filter_by(id=user_id)
        id_prod = id
        if not id:
            raise ValueError(101)
        product = Products.query.filter_by(id=id_prod,availibility=1).first()
        if not product:
            raise ValueError(111)
        modified_by = current_user
        product.availibility = 0
        product.modified_by = modified_by
        db.session.commit()
        return jsonify({"errorCode":0, "errorMessage":"Product marked as inactive"})

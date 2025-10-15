from flask_restful import Resource
from flask import request,jsonify
from flasgger import swag_from
from helper import create_specs_from_schema_product,validateswaggerinput,DB_CONFIG,token_required
from schemas import GetProdSchema
from PIL import Image
from models import Products,db 

class GetImage(Resource):
    specs_dict = create_specs_from_schema_product(GetProdSchema, summary="Getting image of any product that exist", tag="Product", method="GET")
    @swag_from(specs_dict)
    @token_required     
    def get(self,product_id=None, **kwargs):
        current_user = kwargs.get('current_user')
        data = request.args.to_dict()
        id_prod = product_id
        if id==None:
            return jsonify({"errorCode":1, "errorMessage":"Please put id in url after the endpoint"})
        validateerror = validateswaggerinput(GetProdSchema,data)
        if validateerror:
            return validateerror
        if not id:
            raise ValueError(101)
        url = Products.query.filter_by(id=id_prod, availability=1).first()
        if not url:
            raise ValueError(111)  
        image_url = url.image
        try:
            image = Image.open(image_url)
            image.show()
        except Exception:
            raise ValueError(116)
        return jsonify({"errorCode":0, "errorMessage":f"Image opened successfully by {current_user}"})

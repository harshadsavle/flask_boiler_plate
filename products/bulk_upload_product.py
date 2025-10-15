from flask_restful import Resource
from flask import request,jsonify,Response
from helper import create_specs_from_schema_product, validateswaggerinput,DB_CONFIG,token_required
from schemas import NewProdSchema
from schemas import BulkUploadProductSchema
from flasgger import swag_from
from models import Products,db
import csv
from io import StringIO
from sqlalchemy import insert

class BulkUploadProduct(Resource):

    specs_dict = create_specs_from_schema_product(BulkUploadProductSchema, summary="Bulk uploading products", tag="Extra Product Features",requires_file=True, method="POST")
    @swag_from(specs_dict)
    @token_required
    def post(self,**kwargs):   
        owner = kwargs.get('user_id') 
        csv_data = request.files.get('file').read()
        response = Response(csv_data, mimetype="text/csv")
        response.headers["Content-Disposition"] = 'attachment; filename="somefilename.csv"'
        decoded_csv = csv_data.decode('utf-8')
        csv_file = StringIO(decoded_csv)
        csv_reader = csv.DictReader(csv_file)
        data_as_dict = []
        for row in csv_reader:
            row['owner_id'] = owner  # Add owner_id to each row
            data_as_dict.append(row)
        db.session.execute(insert(Products), data_as_dict)
        db.session.commit()
        return response

        
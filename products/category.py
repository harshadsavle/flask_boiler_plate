from flask import request,jsonify
from flask_restful import Resource
from helper import token_required,create_specs_from_schema_user
from flasgger import swag_from
from models import db,Products
from schemas import CategorySchema

class GetCategory(Resource):
    specs_dict = create_specs_from_schema_user(CategorySchema, summary="Getting all categories", tag="Product", method="put")
    @swag_from(specs_dict)
    @token_required
    
    def get(self,**kwargs):
        distinct_categories = db.session.query(Products.category).distinct().all()
        category_list = []
        for category in distinct_categories:
            category_list.append(category[0])

        return jsonify({"categories":category_list})

from flask_restful import Resource
from flask import request,jsonify
from flasgger import swag_from
from helper import create_specs_from_schema_product,DB_CONFIG,token_required,validateswaggerinput
from schemas import SearchProductSchema
from models import Products,db,UserHistory

def get_values(data):
    category = data.get('category')
    minimumprice = data.get('minimumprice')
    maximumprice = data.get('maximumprice')
    name = data.get("name")
    return category,minimumprice,maximumprice,name

def add_to_user_history(name,user_id):
    product_exist = UserHistory.query.filter_by(searched_keywword = name).first()
    if product_exist:
        product_exist.times_searched = int(product_exist.times_searched)+1
    else:
        new_entry = UserHistory(
            user_id = user_id,
            searched_keyword = name,
            times_searched = 1,
        )
        db.session.add(new_entry)
    db.commit()

def filter_using_condition(category, minimumprice, maximumprice, name):
    largest_negative = 0
    largest_positive = 999999999

    query = Products.query
    if name:
        query = query.filter(Products.name == name)
    
    if category:
        query = query.filter(Products.category == category)
    
    query = query.filter(
        Products.price >= (int(minimumprice) if minimumprice else largest_negative),
        Products.price <= (int(maximumprice) if maximumprice else largest_positive),
        Products.availability == 1 
    )

    products = query.all()
    
    return products


class SearchProduct(Resource):
    specs_dict = create_specs_from_schema_product(SearchProductSchema, summary="Searching item with filters", tag="Product", parametertype="query")
    @token_required
    @swag_from(specs_dict)

    def get(self,**kwargs):
        data = request.args
        category, minimumprice, maximumprice,name = get_values(data)
        products = filter_using_condition(category,minimumprice,maximumprice,name=name)
        dict_items = []
        for product in products:
            dict_items.append({
                "id":product.id,
                "name":product.name,
                "image_url" : product.image,
                "price": product.price,
                "availability" : product.availability,
                "quantity" : product.quantity,
                "updated_at" : product.updated_at,
                "owner_id" : product.owner_id
            })
        return jsonify({"items":dict_items})
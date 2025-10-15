from flask_restful import Resource
from flask import request,jsonify
from flasgger import swag_from
from helper import create_specs_from_schema_product,DB_CONFIG,token_required,validateswaggerinput
from schemas import GetProdSchema
from models import Products,db,UserHistory

def get_values(data):
    category = data.get('category')
    minimumprice = data.get('minimumPrice')
    maximumprice = data.get('maximumPrice')
    return category,minimumprice,maximumprice

def add_to_user_history(product_id,user_id):
    product_exist = UserHistory.query.filter_by(product_id = product_id).first()
    if product_exist:
        product_exist.times_searched = int(product_exist.times_searched)+1
    else:
        new_entry = UserHistory(
            user_id = user_id,
            product_id = product_id,
            times_searched = 1,
        )
        db.session.add(new_entry)
    db.commit()

class GetProduct(Resource):
    specs_dict = create_specs_from_schema_product(GetProdSchema, summary="Getting details about a particular product or the list of all items", tag="Product", method="query")
    @token_required
    @swag_from(specs_dict)

    def get(self, product_id=None, **kwargs):
        user_id = kwargs.get('user_id')
        id_prod = product_id
        if not id_prod:
            product = Products.query.filter_by(availability=1).all()
        else:
            product = Products.query.filter_by(id=id_prod, availability=1).first()
            if not product:
                raise ValueError(118)
            add_to_user_history(product.id, user_id)
            product = [ product ]
        dict_items = []
        for product in product:
            dict_items.append({
                "id":product.id,
                "name":product.name,
                "category" : product.category,
                "image_url" : product.image,
                "price": product.price,
                "availability" : product.availability,
                "quantity" : product.quantity,
                "updated_at" : product.updated_at,
                "modified_by" : product.owner_id,
                "description" : product.description,
                "ratings" : product.ratings,
            })
        return jsonify({"items":dict_items})
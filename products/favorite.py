from flask import jsonify,request
from flask_restful import Resource
from flasgger import swag_from
from sqlalchemy import exists
from models import UserHistory,db
from helper import create_specs_from_schema_product, token_required,create_specs_from_schema_user
from schemas import FavoritesSchema,GetFavoriteSchema

class Favorite(Resource):
    specs_dict = create_specs_from_schema_product(FavoritesSchema, summary="Marking any product as a favorite", tag="Extra Product Features", method="POST", parametertype="path")
    @token_required
    @swag_from(specs=specs_dict)
    def post(self, product_id=None, **kwargs):
        history_exist = db.session.query(exists().where(UserHistory.product_id == product_id)).scalar()
        user_id = kwargs.get('user_id')
        if not history_exist:
            new_entry = UserHistory(
                user_id = user_id,
                product_id = product_id
            )
            db.session.add(new_entry)
        history_obj = UserHistory.query.filter_by(product_id =product_id).first()

        if history_obj.is_favorite==0:
            history_obj.is_favorite=1
            message = "Product added to Favorites"
            action = "added"
        else:
            history_obj.is_favorite = 0
            message = "Product removed from Favorites"
            action = "removed"
        db.session.commit()
        return jsonify({"errorCode":0, "errorMessage":message, "action": action})
    

class GetFavorites(Resource):
    specs_dict = create_specs_from_schema_user(GetFavoriteSchema, summary="Getting favorites of a user", tag="Extra Product Features", method="GET",tokenrequired=True)
    @token_required
    @swag_from(specs=specs_dict)
    
    def get(self,**kwargs):
        user_id = kwargs.get('user_id')
        favorite = UserHistory.query.filter(UserHistory.user_id == user_id, UserHistory.isFavorite==1).all()
        favorite = [product.product_id for product in favorite]
        return jsonify({"Favorites" : favorite})


        
        

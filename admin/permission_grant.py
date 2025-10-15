from flask import jsonify,request
from flask_restful import Resource
from helper import create_specs_from_schema_product,token_required
from flasgger import swag_from
from schemas import PermissionGrantScehema
from models import Permissions,db



class PermissionGrant(Resource):

    specs_dict = create_specs_from_schema_product(PermissionGrantScehema, summary="Granting permissions to a particular role", tag="Admin", method="POST")
    @swag_from(specs_dict)
    @token_required

    def post(self,**kwargs):
        role_id_user = kwargs.get('role')
        if role_id_user!=3:
            raise ValueError(126)
        data = request.form
        role_id = data.get('role_id')
        method = data.get('method').upper()
        status = data.get('status')
        endpoint = data.get('endpoint')
        permission_exist = Permissions.query.filter_by(role_id = role_id, method = method, endpoint = endpoint).first()
        if not permission_exist:
            permission_obj = Permissions(
                role_id = role_id,
                method = method,
                endpoint = endpoint,
                status = 1
            )
            db.session.add(permission_obj)
        else:
            permission_exist.status = status
        db.session.commit()
        return jsonify({"errorCode":0, "errorMessage":"Successfully permission modified"})




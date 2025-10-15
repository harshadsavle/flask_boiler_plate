from marshmallow import fields,Schema,validate


#USER APIs
class SignupSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1,max=20))
    email = fields.Email(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))
    address = fields.Str(validate=validate.Length())

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))

class ChangeSchema(Schema):
    oldpassword = fields.Str(required=True, validate=validate.Length(min=6))
    newpassword = fields.Str(required=True, validate=validate.Length(min=6))


#PRODUCT APIs
class NewProdSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    price = fields.Int(required=True)
    quantity = fields.Int(required=True)
    category = fields.String(validate=validate.Length(min=3))

class UpdateProdSchema(Schema):
    id = fields.Integer(required=True)
    price = fields.Int()
    quantity = fields.Int()

class GetProdSchema(Schema):
    id = fields.Integer(required=False)
    

class ChangeQuantSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length())
    quantity = fields.Int(required=True)
    method = fields.Str(required=True, validate=validate.Length())

class DeleteProdSchema(Schema):
    id = fields.Int(required=False)

class FavoritesSchema(Schema):
    product_id = fields.Integer(required=False)

class AddToCartSchema(Schema):
    id = fields.Int()

class PurchaseSchema(Schema):
    payment_confirm = fields.String(required=True)
    total_price = fields.Int(required=True)
    purchase_list = fields.List(fields.Dict())

class ProfileSchema(Schema):
    pass

class UpdateStatusSchema(Schema):
    id_purchase = fields.Int(required=True)
    status = fields.Str()
    shipped_on = fields.Str()
    delivered_on = fields.Str()

class SearchProductSchema(Schema):
    name = fields.Str()
    minimumprice = fields.Integer(required=False)
    maximumprice = fields.Integer(required=False)
    category = fields.String(required=False)

class AddCouponsSchema(Schema):
    code = fields.String(validate=validate.Length(min=5))
    discount = fields.Integer()

class CategorySchema(Schema):
    pass

class BulkUploadProductSchema(Schema):
    pass

class GetFavoriteSchema(Schema):
    pass

class PermissionGrantScehema(Schema):
    role_id = fields.Integer(required=True)
    method = fields.String(required=True)
    endpoint = fields.String(required=True)
    status = fields.String(required=False)

class SampleCSVBulkProductSchema(Schema):
    pass

class UpdateCartProductSchema(Schema):
    product_id = fields.Int(required=False)
    remove = fields.Bool(required=True)
    quantity = fields.Int(required=False)

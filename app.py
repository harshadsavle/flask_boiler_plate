from flask import Flask, request,g, jsonify
from flask_restful import Api
from users import changepassword, signup, login, profile
from products import get_update_delete,get_image, get_product,add_to_cart,purchase,search_product,category,favorite,bulk_upload_product,sample_csv,update_cart_quantity
from admin import update_status,add_coupons, new_prod,permission_grant
import time, os
from dotenv import load_dotenv
from logger import logger
from error_handler import ErrorHandlingMiddleware
from flasgger import Swagger
from flask_cors import CORS
from models import db

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
AUTH_KEY = os.getenv('AUTH_KEY')
DB_CONFIG = {
    "host": os.getenv('DB_HOST'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "database": os.getenv('DB_DATABASE')
}


# Creating a cursor object
app = Flask(__name__)
api = Api(app)

#Important - doesn't connect to network without CORS
CORS(app)

SECRET_KEY = os.getenv('SECRET_KEY')

DEFAULT_ENDPOINT = 'apispec_1'

DEFAULT_CONFIG = {
        # "basePath" : os.getenv("BASE_URL"),
        "title":"User and Product API",
        "termsOfService" : None,
        "description" : "This page contain several APIs for User Authentication and to access Product Database",
        "headers": [    
        ],
        "specs": [
        {
            "endpoint": DEFAULT_ENDPOINT,
            "route": f'/{DEFAULT_ENDPOINT}.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
        "static_url_path": "/flasgger_static",
        # "static_folder": "static",  # must be set by user
        "swagger_ui": True,
        "specs_route": "/swagger/",
        "securityDefinitions": {
        # "Bearer": {
        #     "type": "apiKey",
        #     "name": "Authorization",
        #     "in": "header",
        #     "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        # }
    },
    # "security": [{"Bearer": []}]
    }


config=DEFAULT_CONFIG
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:3306/{DB_CONFIG['database']}"
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)

swagger = Swagger(app,config=config)

errorHandle = ErrorHandlingMiddleware(app)


API_ENDPOINT = '/product'

api.add_resource(login.Login , '/login')
api.add_resource(changepassword.ChangePassword, '/changepassword')
api.add_resource(signup.Signup, '/signup')
api.add_resource(get_update_delete.GetDeleteUpdateProd,'/product/<int:product_id>')
api.add_resource(new_prod.NewProd, '/product')
api.add_resource(get_product.GetProduct, '/productlist')
api.add_resource(get_image.GetImage,'/product/image/<int:product_id>')
api.add_resource(add_to_cart.AddToCart, '/product/addtocart/<int:product_id>')
api.add_resource(purchase.BuyNow, '/product/buynow')
api.add_resource(purchase.AfterPayment, '/product/purchase/webhook')
api.add_resource(profile.Profile, '/user')
api.add_resource(update_status.UpdateStatus, '/admin/updatestatus')
api.add_resource(search_product.SearchProduct, '/product/search')
api.add_resource(add_coupons.AddCoupons, '/admin/addcoupon')
api.add_resource(category.GetCategory, '/category')
api.add_resource(favorite.Favorite, '/favorite/<int:product_id>]')
api.add_resource(favorite.GetFavorites, '/getfavorite')
api.add_resource(bulk_upload_product.BulkUploadProduct, '/bulkupload')
api.add_resource(permission_grant.PermissionGrant, '/permission')
api.add_resource(sample_csv.SampleCSVBulkProduct, '/samplecsv')
api.add_resource(update_cart_quantity.UpdateCartProduct, '/updatecart')


@app.before_request
def getstarttime():
    g.start = time.time()


@app.after_request
def getelapsetime(response):
    elapse_time = ""
    elapse_time = time.time() - g.start

    # if "product" in request.path or "changepassword" in request.path:
    #     auth_token = request.headers['token']
    #     connection = mysql.connector.connect(**DB_CONFIG)
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT * FROM tokens WHERE token = %s", (auth_token,))
    #     result = cursor.fetchall()
    #     if not result:
    #         return jsonify({"errorCode":1, "errorMessage":"You are not authenticated"})
    # Only process JSON responses
    if response.content_type == "application/json":
        extralogdata = {
            "methodName" : request.method,
            "client_ip": request.remote_addr,
            "port": request.environ.get('SERVER_PORT'),
            "data": request.get_json(silent=True),  # 'silent=True' prevents errors if there's no JSON
            "time_taken": time.time(),
            "elapse_time": elapse_time,
        }
        
        logger.info(response.get_json().get('errorMessage'), extra=extralogdata)
    return response




if __name__ == '__main__':
    app.run(debug=True)
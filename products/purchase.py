from flask_restful import Resource
from flask import request,jsonify
from helper import create_specs_from_schema_product,token_required,validateswaggerinput
from schemas import PurchaseSchema
from flasgger import swag_from
from models import Products,Users,Coupons
import random
import json
import string
import stripe


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits  # Includes both uppercase, lowercase letters, and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def check_product_exist(id_prod):
    result = Products.query.filter_by(id=id_prod,availability=1).first()
    if not (result):
        raise ValueError(111)

def get_values(form):
    total_price = form.get('total_price')
    payment_confirm = form.get('paymentConfirm')
    purchase_list = form.get('purchase_list')
    return total_price,payment_confirm,purchase_list

def get_discounted_price(coupon,price):
    if not coupon:
        return price
    coupon_exist = Coupons.query.filter_by(code=coupon).first()
    if not coupon_exist:
        raise ValueError(129)
    discount = coupon_exist.discount
    discount_value = price*int(discount)/100
    discounted_price = price-discount_value
    return discounted_price


def initiate_stripe_payment(purchase_list):
    stripe.api_key = "test api key"
    
    items = [
        {"unit_amount": 20000, "product_name": "Mobile"},
        {"unit_amount": 30000, "product_name": "Refrigerator"},
        {"unit_amount": 780, "product_name": "Bag"},
        {"unit_amount": 57000, "product_name": "Laptop"},
        {"unit_amount": 13000, "product_name": "PC"},
    ]
    
    price_ids = {}
    for item in items:
        product = stripe.Product.create(name=item["product_name"])
        
        price = stripe.Price.create(
            currency="inr",
            unit_amount=item["unit_amount"],
            product=product.id,
        )
        
        price_ids[item.get("product_name")] = {"product_id" : product.id, "price_id" :price}
    line_items = []
    for purchase in purchase_list:
        product_id = purchase.get("id")
        quantity = purchase.get("quantity")
        
        price_id = price_ids.get(purchase.get("name"))['price_id']
        if price_id:
            line_items.append({
                "price": price_id,
                "quantity": quantity
            })
        else:
            print(f"Product ID {product_id} not found in created products.")
    print(line_items)
    session = stripe.checkout.Session.create(line_items=line_items,  mode="payment",  success_url="http://localhost:3000/profile",)

    return session




class BuyNow(Resource):

    specs_dict = create_specs_from_schema_product(PurchaseSchema, summary="Buying a new product", tag="Purchase")
    @swag_from(specs_dict)
    @token_required
    def post(self,**kwargs):
        user_id = kwargs.get('user_id')
        purchase_obj_list = []
        cart_obj_list = []
        userobj = Users.query.filter_by(id=user_id).first()
        balance = userobj.balance
        data = request.form
        total_price,payment_confirm,purchase_list = get_values(data)
        purchase_list = json.loads(purchase_list)
        if not balance:
            raise ValueError(127)
        if int(total_price)>int(balance):
            raise ValueError(124)
        stripe_url = initiate_stripe_payment(purchase_list=purchase_list)
        # purchase_code = generate_random_string()
        # for item in purchase_list:
        #     if item.get("quantity")==0:
        #         continue
        #     product_id = item.get("id")
        #     product_obj  = Products.query.filter_by(id=item.get("id")).first()
        #     check_product_exist(product_id)
        #     purchase = Purchase(
        #         user_id = user_id,
        #         product_id = item.get("id"),
        #         ordered_on = datetime.now(),
        #         status = "Ordered",
        #         purchase_code = purchase_code,
        #         quantity = item.get("quantity"),
        #     )
        #     cart_entry = CartPurchase(
        #         user_id = user_id,
        #         status = "purchase",
        #         purchase_code = purchase_code,
        #         product_id = item.get("id"),
        #     )
        #     cart_entry_for_same_buy = CartPurchase.query.filter_by(user_id = user_id, product_id = item.get("id"))
        #     cart_entry_for_same_buy.delete()
        #     product_obj.quantity = int(product_obj.quantity)-item.get("quantity")
        #     purchase_obj_list.append(purchase)
        #     cart_obj_list.append(cart_entry)
        # newbalance = int(userobj.balance) - int(total_price)
        # userobj.balance = newbalance
        # db.session.add_all(purchase_obj_list)
        # db.session.add_all(cart_obj_list
        # )
        # db.session.commit()
        return jsonify({"errorCode": 0, "errorMessage" : str(stripe_url.url)})  


class AfterPayment(Resource):
    def post(self):
        endpoint_secret = "whsec_ppSMzl4h9mRgdx4ZMSoc3qHNtEy5PSWj"
        event = None
        payload = request.data

        try:
            event = json.loads(payload)
        except json.decoder.JSONDecodeError as e:
            print('⚠️  Webhook error while parsing basic request.' + str(e))
            return jsonify(success=False)
        if endpoint_secret:
            # Only verify the event if there is an endpoint secret defined
            # Otherwise use the basic event deserialized with json
            sig_header = request.headers.get('stripe-signature')
            print(sig_header)
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, endpoint_secret
                )
            except stripe.error.SignatureVerificationError as e:
                print('⚠️  Webhook signature verification failed.' + str(e))
                return jsonify(success=False)

        # Handle the event
        if event and event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
            print('Payment for {} succeeded'.format(payment_intent['amount']))
            # Then define and call a method to handle the successful payment intent.
            # handle_payment_intent_succeeded(payment_intent)
        elif event['type'] == 'payment_method.attached':
            payment_method = event['data']['object']  # contains a stripe.PaymentMethod
            # Then define and call a method to handle the successful attachment of a PaymentMethod.
            # handle_payment_method_attached(payment_method)
        else:
            # Unexpected event type
            print('Unhandled event type {}'.format(event['type']))

        return jsonify(success=True)

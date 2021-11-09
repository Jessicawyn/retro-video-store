from app import db
from app.models.customer import Customer
from flask import Blueprint, json, jsonify, make_response, request, abort
from datetime import datetime


customer_bp = Blueprint("customer", __name__, url_prefix="/customers")

#Helper Functions 
def valid_int(number, parameter_type):
    try:
        int(number)
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))


def get_customer_from_id(customer_id):
    valid_int(customer_id, "customer_id")

    customer = Customer.query.get(customer_id)
    if not customer:
        abort(make_response({"message": f"Customer {customer_id} was not found"}, 404)) 
    return customer



#ROUTES
@customer_bp.route("", methods=["GET"])
def read_all_customers():
    customers = Customer.query.all()

    customer_response = []
    for customer in customers:
        customer_response.append(
            customer.to_dict()
        )
    return jsonify(customer_response)
   

#GET ONE CUSTOMER WITH ID
@customer_bp.route("/<customer_id>", methods=["GET"])
def read_task(customer_id):
    customer = get_customer_from_id(customer_id)
    return make_response(customer.to_dict(), 200)


# CREATE ONE CUSTOMER
@customer_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    if "name" not in request_body:
        return {"details": "Request body must include name."}, 400
    if "postal_code" not in request_body:
        return {"details": "Request body must include postal_code."}, 400
    if "phone" not in request_body:
        return {"details": "Request body must include phone."}, 400

    new_customer = Customer(
        name=request_body["name"],
        postal_code=request_body["postal_code"],
        phone=request_body["phone"],
        registered_at = datetime.utcnow()
        )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.to_dict(), 201)


#UPDATES AND RETUNS DETAILS ABOUT SPECIFIC CUSTOMER
@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = get_customer_from_id(customer_id)

    request_body = request.get_json()
    
    if "name"  not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return make_response({"message": "Invalid data" }, 400)
    else:
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
 
    
    db.session.commit()
    return make_response(customer.to_dict(), 200)


#DELETE A CUSTOMER
@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer =  get_customer_from_id(customer_id)

    db.session.delete(customer)
    db.session.commit()
    return make_response({"id":int(customer_id)}, 200)

    





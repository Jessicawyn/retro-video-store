from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from flask import Blueprint, json, jsonify, make_response, request, abort
from datetime import datetime
from app.common_functions.check_for_id import valid_int, get_id
from app.common_functions.read_all import read_all
from app.common_functions.check_request_body import chek_request_body
    


customer_bp = Blueprint("customer", __name__, url_prefix="/customers")        

#ROUTES
@customer_bp.route("", methods=["GET"])
def read_all_customers():

    name_query = request.args.get("name")
    registered_at_query = request.args.get("registered_at")
    postal_code_query = request.args.get("postal_code")
    sort_query = request.args.get("sort")

    if name_query:
        customers = Customer.query.filter_by(name=name_query)
    elif registered_at_query:
        customers = Customer.query.filter_by(registered_at=registered_at_query)
    elif postal_code_query:
        customers = Customer.query.filter_by(postal_code=postal_code_query)
    else:
        customers = Customer.query.all()

        customer_response = []
        for customer in customers:
            customer_response.append(
                customer.to_dict()
            )
        # customer_response = read_all(Customer)
    return jsonify(customer_response)
   

#GET ONE CUSTOMER WITH ID
@customer_bp.route("/<customer_id>", methods=["GET"])
def read_task(customer_id):
    customer = get_id(customer_id, Customer, str_repr="Customer")
    return make_response(customer.to_dict(), 200)


# CREATE ONE CUSTOMER
@customer_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    request_parameters = ["name", "postal_code", "phone"]
    chek_request_body(request_parameters)

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
    customer = get_id(customer_id, Customer, str_repr="Customer")
    request_body = request.get_json()

    request_parameters = ["name", "postal_code", "phone"]

    for parameter in request_parameters:
        if parameter  not in request_body:
            return make_response({"message": "Invalid data" }, 400)

        else:
            customer.name = request_body["name"]
            customer.postal_code = request_body["postal_code"]
            customer.phone = request_body["phone"]

        # else:
        #     customer.parameter = request_body[parameter]

   
 
    
    db.session.commit()
    return make_response(customer.to_dict(), 200)


#DELETE A CUSTOMER
@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer =  get_id(customer_id, Customer, str_repr="Customer")

    db.session.delete(customer)
    db.session.commit()
    return make_response({"id":int(customer_id)}, 200)
    

#LIST THE VIDEOS A CUSTOMER CURRENTLY HAS CHECKED OUT
@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_rentals(customer_id):
    customer = get_id(customer_id, Customer, str_repr="Customer")

    return make_response(jsonify(customer.to_dict_with_rentals()), 200)


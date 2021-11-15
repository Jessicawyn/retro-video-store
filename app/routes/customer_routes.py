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

    sort_query = request.args.get("sort")
    page = request.args.get('p', 1, type=int)
    per_page = request.args.get('n', 10, type=int)

    if sort_query == "name":
        customers = Customer.query.order_by(Customer.name.asc()).paginate(page=page, per_page=per_page)
    elif sort_query == "registered_at":
        customers = Customer.query.order_by(Customer.registered_at.asc()).paginate(page=page, per_page=per_page)
    elif sort_query == "postal_code":
        customers = Customer.query.order_by(Customer.postal_code.asc()).paginate(page=page, per_page=per_page)
    else:
        customers = Customer.query.order_by(Customer.id.asc()).paginate(page=page, per_page=per_page)
    
    paginated_customers = customers.items

    customer_response = []
    for customer in paginated_customers:
        customer_response.append(
            customer.to_dict()
            )

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


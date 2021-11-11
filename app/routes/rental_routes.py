from flask import Blueprint, jsonify, make_response, request, abort
from flask.helpers import make_response
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from app import db
from datetime import datetime, timedelta

rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

# Helper Functions
def valid_int(number, parameter_type):
    try:
        if int(number) < 0:
            abort(make_response({"error": f"{parameter_type} cannot be a negative int"}, 400))
    
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))

def get_id(id, model):
    valid_int(id, "id")
    rental = model.query.get(id)
    if not rental:        
        abort(make_response({"message": f"Rental {id} was not found"}, 404))
    return rental




    
#POST/RENTALS/CHECK-OUT

@rental_bp.route("/check-out", methods=["POST"])
def create_rental():

    request_body = request.get_json()
    request_body_parameters = ["customer_id", "video_id"]
    for parameter in request_body_parameters:
        if parameter not in request_body:
            abort(make_response({"details": f"Request body must include {parameter}."}, 400))

    
    get_id(request_body["customer_id"],Customer)
    get_id(request_body["video_id"], Video)

    new_rental = Rental(
        customer_id = request_body["customer_id"],
        video_id = request_body["video_id"], 
        due_date = datetime.utcnow() + timedelta(7)
    )


    db.session.add(new_rental)
    db.session.commit()

    
    avilable_inventory = new_rental.get_available_inventory()
    print(avilable_inventory )
    if   avilable_inventory  < 0:
        print("abort")
        abort(make_response({"message": "Could not perform checkout."}, 400))

    return make_response(new_rental.to_dict(),200)



#LIST THE VIDEOS A CUSTOMER CURRENTLY HAS CHECKED OUT
# @rental_bp.route("/<customer_id>/rentals", methods=["GET"])
# def get_rentals():

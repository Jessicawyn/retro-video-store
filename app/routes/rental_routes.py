from flask import Blueprint, jsonify, make_response, request, abort
from flask.helpers import make_response
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from app import db
from datetime import datetime, timedelta
from app.common_functions.check_for_id import valid_int, get_id
from app.common_functions.check_request_body import chek_request_body

rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

# Helper Functions

    
#POST/RENTALS/CHECK-OUT

@rental_bp.route("/check-out", methods=["POST"])
def create_rental():
    request_body = request.get_json()
    
    request_body_parameters = ["customer_id", "video_id"]
    chek_request_body(request_body_parameters)
    # for parameter in request_body_parameters:
        # if parameter not in request_body:
        #     abort(make_response({"details": f"Request body must include {parameter}."}, 400))

    
    get_id(request_body["customer_id"],Customer, str_repr="Customer")
    get_id(request_body["video_id"], Video, str_repr="Video")

    new_rental = Rental(
        customer_id = request_body["customer_id"],
        video_id = request_body["video_id"], 
        due_date = datetime.utcnow() + timedelta(7)
    )

    db.session.add(new_rental)
    db.session.commit()

    
    avilable_inventory = new_rental.get_available_inventory()
   
    if   avilable_inventory  < 0:
        abort(make_response({"message": "Could not perform checkout."}, 400))

    return make_response(new_rental.to_dict(),200)


@rental_bp.route("/check-in", methods=["POST"])
def create_check_in():
    request_body = request.get_json()

    request_body_parameters = ["customer_id", "video_id"]
    chek_request_body(request_body_parameters)
    

    video_id = request_body["video_id"]
    customer_id = request_body["customer_id"]

    # Check customer exists in Customer
    check_customer = Customer.query.get(customer_id) 
    if not check_customer:
        return make_response({"message": f"No rentals for customer {customer_id}."}, 404)
    
    # Check video exists in Video
    check_video = Video.query.get(video_id)    
    if not check_video:
        return make_response({"message": f"No rentals for the video {video_id}."}, 404)
    
    # Get rental to check in and ensure it is checked out
    rental_to_check_in = Rental.query.filter(
        Rental.video_id == video_id,
        Rental.customer_id == customer_id,
        Rental.checked_in.is_(None)
        ).first()
    
    if not rental_to_check_in:
        return make_response({"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}, 400)
    
    # Checkin Rental: Add checked_in date and update database
    rental_to_check_in.checked_in = datetime.utcnow()

    db.session.commit()

    # Return rental information
    return make_response(rental_to_check_in.to_dict(), 200)

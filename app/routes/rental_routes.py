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
        abort(make_response({"message": f"{model} {id} was not found"}, 404))
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


@rental_bp.route("/check-in", methods=["POST"])
def create_check_in(): # TODO: Make this a helper function as it's called in both routes
    request_body = request.get_json()
    request_body_parameters = ["customer_id", "video_id"]
    for parameter in request_body_parameters:
        if parameter not in request_body:
            abort(make_response({"details": f"Request body must include {parameter}."}, 400))


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
    rental_to_check_in.checked_in == datetime.utcnow()

    db.session.commit()

    # rental_to_check_in.

    # Return rental information

    return make_response(rental_to_check_in.to_dict(),200)
    # return make_response("RTURN ",200)
    #     )
    # # total_inventory = video["total_inventory"] filter(myModel.border.is_(None))
    # checked_out = Rental.query.filter(Rental.video_id == video_id, Rental.checked_in.border.is_(None))
    # checked_out = Rental.query.filter(Rental.checked_in.border.is_(None))
    # checked_in = Rental.query.filter(Rental.checked_in.isnot(None))
    # checked_out = Rental.query.filter(Rental.video_id == video_id, Rental.checked_in.is_(None))
    # # Rental.checked_in.is_(None), Rental.video_id == video_id))
    # working = Rental.query.filter(Rental.video_id == video_id)


    

    # return make_response("", 200)
    # response_body = {
    #     "customer_id": customer_id,
    #     "video_id": video_id,
    #     "videos_checked_out_count": customer_video_checkout_count(customer_id),
    #     "available_inventory": get_available_inventory(video_id)
    #     }
    # return make_response(jsonify(working_list), 200)
    # return make_response(f"rental id hello", 200)


# len(video.rentals) video.rentals - list of all rentals with that video id
#                                     rental objects

# rental.video 

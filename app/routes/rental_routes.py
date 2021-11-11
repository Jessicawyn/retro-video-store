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
    if "customer_id" not in request_body:
        abort(make_response({"details": "Request body must include customer_id."}, 400))
    elif "video_id" not in request_body:
        abort(make_response({"details": "Request body must include video_id."}, 400))
    
    get_id(request_body["customer_id"],Customer)
    get_id(request_body["video_id"], Video)

    new_rental = Rental(
        customer_id = request_body["customer_id"],
        video_id = request_body["video_id"], 
        due_date = datetime.utcnow() + timedelta(7)
    )


    db.session.add(new_rental)
    db.session.commit()

    
    # rentals_checked_out_by_customer = Rental.query.filter_by(customer_id=request_body["customer_id"]).all() 
    # print(f"rentals_checked_out_by_customer{rentals_checked_out_by_customer}")
    # rentals_with_the_video = Rental.query.filter_by(video_id=request_body["video_id"]).all() 
    # available_videos = [video for video in rentals_with_the_video if video.checked_in == None]

    # rentals_with_the_video = Rental.query.filter(
    
    # avilable_inventory = new_rental.get_available_inventory()
    # print(avilable_inventory )
    # if   avilable_inventory  < 0:
    #     print("abort")
    #     abort(make_response({"message": "Could not perfom checkout."}, 404))
        
    
    # print("******")
    
    # print(new_rental.to_dict())
    return make_response(new_rental.to_dict(),200)

   



#LIST THE VIDEOS A CUSTOMER CURRENTLY HAS CHECKED OUT
# @rental_bp.route("/<customer_id>/rentals", methods=["GET"])
# def get_rentals():

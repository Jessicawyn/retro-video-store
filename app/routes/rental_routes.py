from flask import Blueprint, jsonify, make_response, request, abort
from flask.helpers import make_response
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from app import db
from datetime import datetime, timedelta
from .video_routes import get_video_from_id
from sqlalchemy.sql.expression import text

rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

# Helper Functions
def valid_int(number, parameter_type):
    try:
        if int(number) < 0:
            abort(make_response({"error": f"{parameter_type} cannot be a negative int"}, 400))
    
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))

def get_rental_from_id(rental_id):
    valid_int(rental_id, "rental_id")
    rental = Rental.query.get(rental_id)
    if not rental:        
        abort(make_response({"message": f"Rental {rental_id} was not found"}, 404))
    return rental


def valid_request_body_inputs():
    request_body = request.get_json()
    if "customer_id" not in request_body:
        abort(make_response({"details": "Request body must include customer_id."}, 400))
    elif "video_id" not in request_body:
        abort(make_response({"details": "Request body must include video_id."}, 400))
    return request_body

def get_available_inventory(video_id):
    video = get_video_from_id(video_id)
    video_dict = video.to_dict()
    total_inventory = video_dict["total_inventory"]

    checked_out = Rental.query.filter(Rental.video_id == video_id, Rental.checked_in.is_(None))
    checked_out_list = []
    for rental in checked_out:
        checked_out_list.append(
            rental.to_dict()
        )

    return total_inventory - len(checked_out_list)

def customer_video_checkout_count(customer_id):
    checked_out = Rental.query.filter(Rental.customer_id == customer_id, Rental.checked_in.is_(None))
    checked_out_list = []
    for rental in checked_out:
        checked_out_list.append(
            rental.to_dict()
        )
    return len(checked_out_list)

#POST/RENTALS/CHECK-OUT

@rental_bp.route("/check-out", methods=["POST"])
def create_rental():
    request_body = request.get_json()
    if "customer_id" not in request_body:
        abort(make_response({"details": "Request body must include customer_id."}, 400))
    elif "video_id" not in request_body:
        abort(make_response({"details": "Request body must include video_id."}, 400))
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    new_rental = Rental(
        customer_id = request_body["customer_id"],
        video_id = request_body["video_id"], 
        due_date = datetime.utcnow() + timedelta(7)
    )

    db.session.add(new_rental)
    db.session.commit()

    


    #     {
    # "customer_id": 122581016,
    # "video_id": 235040983,
    # "due_date": "2020-06-31",
    # "videos_checked_out_count": 2,
    # "available_inventory": 5
    # }
    
    return make_response("CREATE RESPONSE HERE", 201)

@rental_bp.route("/check-in", methods=["POST"])
def create_check_in():
    request_body = valid_request_body_inputs()

    video_id_please = request_body["video_id"]
    customer_id = request_body["customer_id"]

    # Check for video and customer in rentals
    # TODO: Create Helper Function For List loops
    check_customer = Customer.query.get(customer_id) 
    # customer_rentals_list = []
    # for customer in check_customer:
    #     customer_rentals_list.append(customer)

    if not check_customer:
        return make_response({"message": f"No rentals for customer {customer_id}."}, 404)
    # customer_rentals = Rental.query.filter(Rental.customer_id == request_body["customer_id"]) 
    # customer_rentals_list = []
    # for customer in customer_rentals:
    #     customer_rentals_list.append(customer)

    # if len(customer_rentals_list) == 0 :
    #     return make_response({"message": f"No rentals for customer {customer_id}."}, 404)
    check_video = Video.query.get(video_id_please)
    # video_rentalsx_list = []
    # for video in check_video:
        # video_rentals_list.append(video)
    
    if not check_video:
        return make_response({"message": f"No rentals for the video {video_id_please}."}, 404)

    
    # video_rentals = Rental.query.filter(Rental.video_id == video_id_please)
    # video_rentals_list = []
    # for video in video_rentals:
    #     video_rentals_list.append(video)
    
    # if len(video_rentals_list) == 0:
    #     return make_response({"message": f"No rentals for the video {video_id_please}."}, 404)
    
    # Checkin Video not checked out
    video_by_customer = Rental.query.filter(
        Rental.video_id == video_id_please,
        Rental.customer_id == customer_id,
        Rental.checked_in.is_(None)
        )
    
    video_by_customer_list = []
    for rentals in video_by_customer:
        video_by_customer_list.append(rentals)

    if len(video_by_customer_list) == 0:
        return make_response({"message": f"No outstanding rentals for customer {customer_id} and video {video_id_please}"}, 400)
    

    # rental_to_check_in = Rental.query.filter(
    #     Rental.customer_id == customer_id,
    #     Rental.video_id == video_id_please
    #     # Rental.checked_in.is_(None)
    #     )

    # if not rental_to_check_in:
    #     return make_response({"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}, 404)

    
    # rental_to_check_in_list = []
    # for rental in rental_to_check_in:
    #     rental_to_check_in_list.append(rental)
    
    # rental_id = rental_to_check_in_list[0].id
    #     new_rental = Rental(
    #     customer_id = request_body["customer_id"],
    #     video_id = request_body["video_id"], 
    #     due_date = datetime.utcnow() + timedelta(7)
    # )

    

    



    # new_rental = Rental(
    #     customer_id = request_body["customer_id"],
    #     video_id = video_id, 
    #     checked_in = datetime.utcnow()
    # )

    # db.session.add(new_rental)
    # # db.session.commit()

    # video = get_video_from_id(video_id_please)

    # video_response = video.to_dict()
    # for v in video:
    #     video_response.append(
    #         video.to_dict()
    #     )
    # # total_inventory = video["total_inventory"] filter(myModel.border.is_(None))
    # checked_out = Rental.query.filter(Rental.video_id == video_id, Rental.checked_in.border.is_(None))
    # checked_out = Rental.query.filter(Rental.checked_in.border.is_(None))
    checked_in = Rental.query.filter(Rental.checked_in.isnot(None))
    checked_out = Rental.query.filter(Rental.video_id == video_id_please, Rental.checked_in.is_(None))
    # Rental.checked_in.is_(None), Rental.video_id == video_id_please))
    working = Rental.query.filter(Rental.video_id == video_id_please)
    working_list = []

    

    for rental in video_by_customer:
        working_list.append(
            rental.to_dict()
        )
    # return make_response(jsonify(working_list), 200)
    # response_body = {
    #     "customer_id": customer_id,
    #     "video_id": video_id_please,
    #     "videos_checked_out_count": customer_video_checkout_count(customer_id),
    #     "available_inventory": get_available_inventory(video_id_please)
    #     }
    # return make_response(jsonify(video_by_customer_list), 200)
    return make_response(f"rental id hello", 200)

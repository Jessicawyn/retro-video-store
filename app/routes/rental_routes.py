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

def get_rental_from_id(rental_id):
    valid_int(rental_id, "rental_id")
    rental = Rental.query.get(rental_id)
    if not rental:        
        abort(make_response({"message": f"Rental {rental_id} was not found"}, 404))
    return rental


#POST/RENTALS/CHECK-OUT

@rental_bp.route("/check-out", methods=["POST"])
def create_rental():
    request_body = request.get_json()
    if "customer_id" not in request_body:
        abort(make_response({"details": "Request body must include customer_id."}, 400))
    elif "video_id" not in request_body:
        abort(make_response({"details": "Request body must include video_id."}, 400))

    new_rental = Rental(
        customer_id = request_body["customer_id"],
        video_id = request_body["video_id"], 
        due_date = datetime.utcnow() + timedelta(7)
    )

    db.seesion.add(new_rental)
    db.session.commit()

    #     {
    # "customer_id": 122581016,
    # "video_id": 235040983,
    # "due_date": "2020-06-31",
    # "videos_checked_out_count": 2,
    # "available_inventory": 5
    # }
    
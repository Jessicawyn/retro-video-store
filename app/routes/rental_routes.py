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

OVERDUE_VALID_SORTS = ["title", "name", "checkout_date", "due_date"]

#POST/RENTALS/CHECK-OUT

@rental_bp.route("/check-out", methods=["POST"])
def create_rental():
    request_body = request.get_json()
    
    request_body_parameters = ["customer_id", "video_id"]
    chek_request_body(request_body_parameters) 

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

    
    check_customer = get_id(customer_id, Customer, "customer")
    check_video = get_id(video_id, Video, "video")
    
    rental_to_check_in = Rental.query.filter(
        Rental.video_id == video_id,
        Rental.customer_id == customer_id,
        Rental.checked_in.is_(None)
        ).first()
    
    if not rental_to_check_in:
        return make_response({"message": f"No outstanding rentals for customer {customer_id} and video {video_id}"}, 400)
    
    rental_to_check_in.checked_in = datetime.utcnow()

    db.session.commit()
    
    return make_response(rental_to_check_in.to_dict(), 200)

@rental_bp.route("/overdue", methods=["GET"])
def get_overdue_rentals():
    sort_query = request.args.get("sort")
    page = request.args.get('p', 1, type=int)
    per_page = request.args.get('n', 10, type=int)
    
    if sort_query and sort_query not in OVERDUE_VALID_SORTS:
        return make_response({"error": "Please enter a valid sort parameter."})
    if sort_query == "checkout_date" or sort_query == "due_date":
        overdue = Rental.query.filter(Rental.checked_in.is_(None), Rental.due_date < datetime.utcnow()).order_by(Rental.due_date.asc()).paginate(page=page, per_page=per_page)
    elif sort_query == "title":
        overdue = Rental.query.filter(Rental.checked_in.is_(None), Rental.due_date < datetime.utcnow()).join(Video).order_by(Video.title.asc()).paginate(page=page, per_page=per_page)
    elif sort_query == "name":
        overdue = Rental.query.filter(Rental.checked_in.is_(None), Rental.due_date < datetime.utcnow()).join(Customer).order_by(Customer.name.asc()).paginate(page=page, per_page=per_page)
    else:
        overdue = Rental.query.filter(Rental.checked_in.is_(None), Rental.due_date < datetime.utcnow()).order_by(Rental.id.asc()).paginate(page=page, per_page=per_page)

    paginated_overdue = overdue.items
    overdue_response = []
    for rental in paginated_overdue:
        overdue_response.append(
            rental.overdue_to_dict()
        )

    return make_response(jsonify(overdue_response), 200)

from flask import Blueprint, jsonify, make_response, request, abort
from flask.helpers import make_response
from app.models.video import Video
from app.models.rental import Rental
from app import db
from datetime import datetime
from app.common_functions.check_for_id import valid_int, get_id
from app.common_functions.read_all import read_all
from app.common_functions.check_request_body import chek_request_body

video_bp = Blueprint("video", __name__, url_prefix="/videos")
VIDEO_VALID_SORTS = ['title', 'release_date']


# Routes
@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    
    request_body_parameters = ["title","release_date","total_inventory"]
    chek_request_body(request_body_parameters)

    new_video = Video(
        title=request_body["title"],
        release_date=request_body["release_date"],
        total_inventory=request_body["total_inventory"]
    )

    db.session.add(new_video)
    db.session.commit()

    return make_response(new_video.to_dict(), 201)

@video_bp.route("", methods=["GET"])
def read_all_videos():

    sort_query = request.args.get("sort")
    page = request.args.get('p', 1, type=int)
    per_page = request.args.get('n', 10, type=int)

    if sort_query and sort_query not in VIDEO_VALID_SORTS:
        return make_response({"error": "Please enter a valid sort parameter."})
        
    if sort_query == "title":
        videos = Video.query.order_by(Video.title.asc()).paginate(page=page, per_page=per_page)
    elif sort_query == "release_date":
        videos = Video.query.order_by(Video.release_date.asc()).paginate(page=page, per_page=per_page)
    else:
        videos = Video.query.order_by(Video.id.asc()).paginate(page=page, per_page=per_page)
    
    paginated_videos = videos.items

    video_response = []
    for video in paginated_videos:
        video_response.append(
            video.to_dict()
        )

    return make_response(jsonify(video_response), 200)


@video_bp.route("/<video_id>", methods=["GET"])
def read_one_video(video_id):
    video = get_id(video_id, Video, str_repr="Video")
    return make_response(video.to_dict(), 200)

@video_bp.route("<video_id>", methods=["PUT"])
def update_video(video_id):
    video = get_id(video_id, Video, str_repr="Video")
    request_body = request.get_json()

    request_body_parameters = ["title","release_date","total_inventory"]
    chek_request_body(request_body_parameters)

    video.title=request_body["title"]
    video.release_date=request_body["release_date"]
    video.total_inventory=request_body["total_inventory"]
    db.session.commit()
    return make_response(video.to_dict(), 200)

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = get_id(video_id, Video, str_repr="Video")
    
    db.session.delete(video)
    db.session.commit()

    return make_response(video.to_dict(), 200)

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def get_rental_customers_by_video(video_id):
    video = get_id(video_id, Video, str_repr="Video")
    return make_response(jsonify(video.to_dict_with_rentals()), 200)
from flask import Blueprint, jsonify, make_response, request, abort
from flask.helpers import make_response
from flask.json import tojson_filter
from flask.signals import request_tearing_down
from werkzeug.exceptions import RequestedRangeNotSatisfiable
from werkzeug.utils import header_property
from app.models.video import Video
from app import db
from datetime import datetime

video_bp = Blueprint("video", __name__, url_prefix="/videos")

# Helper Functions
def valid_int(number, parameter_type):
    try:
        int(number)
    except:
        abort(make_response({"error": f"{parameter_type} must be an int"}, 400))

def get_video_from_id(video_id):
    valid_int(video_id, "video_id")
    try:
        video = Video.query.get(video_id)
    except:
        return None
        # return make_response({"message": f"Video {video_id} was not found"}, 404)
    return video


# Routes
@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Request body must include title."}, 400)
    elif "release_date" not in request_body:
        return make_response({"details": "Request body must include release_date."}, 400)
    elif "total_inventory" not in request_body:
        return make_response({"details": "Request body must include total_inventory."}, 400)
    
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
    videos = Video.query.all()
    video_response = []
    for video in videos:
        video_response.append(
            video.to_dict()
        )
    return make_response(jsonify(video_response), 200)

@video_bp.route("/<video_id>", methods=["GET"])
def read_one_video(video_id):
    video = get_video_from_id(video_id)
    return make_response(video.to_dict(), 200)
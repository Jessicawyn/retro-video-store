from flask import Blueprint, jsonify, make_response, request, abort
from flask.helpers import make_response
from flask.json import tojson_filter
from flask.signals import request_tearing_down
from werkzeug.utils import header_property
from app.models.video import Video
from app import db
from datetime import datetime

video_bp = Blueprint("video", __name__, url_prefix="/videos")


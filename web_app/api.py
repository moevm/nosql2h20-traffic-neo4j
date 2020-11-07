from flask import Blueprint
from flask_restful import Api

from web_app.extensions import csrf_protect
from web_app.resources.map import MapsApi
from web_app.resources.analytics import AnalyticsApi


api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api(api_bp, decorators=[csrf_protect.exempt])

api.add_resource(AnalyticsApi, "/analytics")
api.add_resource(MapsApi, "/map")
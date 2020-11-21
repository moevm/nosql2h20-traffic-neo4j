from flask import jsonify
from flask_restful import Resource

from web_app.db.models import WayNode
from web_app.db.util import find_by_address


class AnalyticsApi(Resource):
    def get(self):
        """
        Method sends to user analytics about database stuff

        Returns:
            response(flask.Response): json with analytics
        """
        start_building = find_by_address(street='Торжковская улица', number='15')
        start_node = WayNode.match(lat=start_building.lat, lon=start_building.lon)
        return jsonify(start_node.__dict__)

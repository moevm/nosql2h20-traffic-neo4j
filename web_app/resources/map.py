from flask import Response, current_app, jsonify, make_response, request
from flask_restful import Resource

from web_app.db.models import WayNode
from web_app.db.util import find_by_address


class MapsApi(Resource):
    def post(self):
        """
        Method receives start and end points,
        calculates the most comfortable path and
        send JSON with the relevant information to user

        Returns:
            response(flask.Response): contains JSON with info about
            the most comfortable path
        """
        try:
            start_street = request.get_json()["start_street"]
            start_number = request.get_json()["start_number"]
            end_street = request.get_json()["end_street"]
            end_number = request.get_json()["end_number"]
            start_building = find_by_address(street=start_street, number=start_number)
            start_node = WayNode.match(lat=start_building.lat, lon=start_building.lon)

            finish_building = find_by_address(street=end_street, number=end_number)
            finish_node = WayNode.match(lat=finish_building.lat, lon=finish_building.lon)

            paths, distances = WayNode.kShortestPaths(id0=start_node.id, id1=finish_node.id)
            return make_response(jsonify([path.__dict__ for path in paths[0]]), 200)
        except TypeError:
            current_app.logger.exception("Received invalid JSON file!")
            return Response("Invalid JSON file!", status=403)
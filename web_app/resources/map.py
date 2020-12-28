from flask import Response, current_app, jsonify, make_response, request
from flask_restful import Resource

from web_app.db.models import WayNode


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

from flask import jsonify
from flask_restful import Resource


class AnalyticsApi(Resource):
    def get(self):
        """
        Method sends to user analytics about database stuff

        Returns:
            response(flask.Response): json with analytics
        """
        # bla bla bla
        return jsonify({'a': 'a'})

"""
Created 12/07/2021
API Status
"""

from flask.wrappers import Response
from app.main.dto import RootDto
from app.main.controllers.resource import Resource

api = RootDto.api


@api.route("/status")
class Status(Resource):
    """ Resource for /status """

    @api.doc("API Status")
    @api.response(200, "Server Status OK")
    def get(self):
        """
        GET /status
        """

        return self.format_success(200, "Pong")

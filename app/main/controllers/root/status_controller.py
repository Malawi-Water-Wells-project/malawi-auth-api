"""
Created 12/07/2021
API Status
"""

from datetime import datetime
from app.main.dto import RootDto
from app.main.controllers.resource import Resource
from os import getloadavg

api = RootDto.api
start_time = datetime.now()


@api.route("/status")
class Status(Resource):
    """ Resource for /status """

    @api.doc("API Status")
    @api.response(200, "Server Status OK")
    def get(self):
        """
        GET /status
        """

        return self.format_success(200, {
            "uptime": (datetime.now() - start_time).seconds,
            "load": getloadavg()
        })

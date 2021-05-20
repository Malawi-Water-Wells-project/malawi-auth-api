"""
Created 20/05/2021
CheckTokenController API Resource
"""
import base64
import json

from app.main.controllers.resource import Resource
from app.main.dto import TribeDto
from app.main.service.tribe_service import check_join_token
from flask.globals import request

api = TribeDto.api


class CheckToken(Resource):
    """ Resource for /tribes/check-token/ """

    def post(self):
        """
        POST /tribes/check-token/
        Checks if a join token is valid, and returns Tribe details if it is
        """
        token = request.json.get("token")

        if token is None:
            return self.format_failure(400, "Token not provided")

        decoded_token = json.loads(base64.b64decode(
            token.encode("ascii")).decode("ascii"))

        is_valid = check_join_token(decoded_token)

        if not is_valid:
            return self.format_failure(400, "Invalid Token")

        return self.format_success(200, {"is_valid": True, "token": decoded_token})

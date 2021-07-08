"""
Created 20/05/2021
CheckTokenController API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import TribeDto
from app.main.service.tribe_service import TribeService
from flask.globals import request

api = TribeDto.api


@api.route("/check-token")
class CheckToken(Resource):
    """ Resource for /tribes/check-token/ """

    def post(self):
        """
        POST /tribes/check-token/
        Checks if a join token is valid, and returns Tribe details if it is
        """
        token_id = request.json.get("token")

        if token_id is None:
            return self.format_failure(400, "Token not provided")

        token = TribeService.lookup_join_token(token_id)

        if token is None:
            return self.format_failure(400, "Invalid Token")

        return self.format_success(200, {"is_valid": True, "token": token.dictionary})

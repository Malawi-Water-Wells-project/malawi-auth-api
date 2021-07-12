"""
Created 20/05/2021
CheckTokenController API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import VillageDto
from app.main.service.village_service import VillageService
from flask.globals import request

api = VillageDto.api


@api.route("/check-token")
class CheckToken(Resource):
    """ Resource for /villages/check-token/ """

    def post(self):
        """
        POST /villages/check-token/
        Checks if a join token is valid, and returns Village details if it is
        """
        token_id = request.json.get("token")

        if token_id is None:
            return self.format_failure(400, "Token not provided")

        token = VillageService.lookup_join_token(token_id)

        if token is None:
            return self.format_failure(400, "Invalid Token")

        return self.format_success(200, {"is_valid": True, "token": token.dictionary})

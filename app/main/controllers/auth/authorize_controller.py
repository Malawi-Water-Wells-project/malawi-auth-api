"""
Created 16/05/2021
Authorize API Resource
"""
from app.main.service.token_service import TokenService
from app.main.controllers.resource import Resource
from app.main.dto import AuthDto
from flask import request

api = AuthDto.api


@api.route("/authorize")
class Authorize(Resource):
    """ Resource for /auth/authorize """

    @api.doc("Refresh Access Token")
    @api.response(400, "No Authorization Header provided")
    @api.response(401, "Invalid Token")
    @api.response(401, "Token Revoked")
    @api.response(404, "User associated with token does not exist")
    def post(self):
        """
        POST /auth/authorize
        Refresh Token required in Authorization header

        generates an Access Token from a Refresh Token
        """
        token = request.headers.get("Authorization")
        if "Bearer" in token:
            token = token.split(" ")[-1]

        if token is None:
            return self.format_failure(400, "No Authorization Header provided")

        details, error = TokenService.decode_refresh_token(token)
        if error or details is None:
            return self.format_failure(401, "Invalid Token")

        record = TokenService.get_refresh_token_record(token)
        if record is None or record.revoked is True:
            return self.format_failure(401, "Invalid Token")

        if details.get("user_id") != record.user_id:
            return self.format_failure(401, "Invalid Token")

        access_token = TokenService.create_access_token(
            user_id=record.user_id,
            role=details.get("role"),
            tribe_id=details.get("tribe_id")
        )

        return self.format_success(200, {"token": access_token})

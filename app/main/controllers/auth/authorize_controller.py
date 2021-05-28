"""
Created 16/05/2021
Authorize API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import AuthDto
from app.main.service.token_service import get_refresh_token
from app.main.service.user_service import UserService
from app.main.util.jwt import generate_access_token, validate_refresh_token
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

        if token is None:
            return self.format_failure(400, "No Authorization Header provided")

        error, _ = validate_refresh_token(token)

        if error is not None:
            return self.format_failure(401, error)

        if "Bearer " in token:
            token = token.split(" ").pop()

        existing_token = get_refresh_token(token)
        if existing_token is None:
            return self.format_failure(401, "Invalid Token")

        if existing_token.revoked:
            return self.format_failure(401, "Token Revoked")

        user = UserService.get_by_id(int(existing_token.user_id))
        if user is None:
            return self.format_failure(404, "User associated with token does not exist")

        access_token = generate_access_token(user.id, user.tribe_id, user.role)

        return self.format_success(200, {
            "token": access_token
        })

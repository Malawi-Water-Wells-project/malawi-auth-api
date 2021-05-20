"""
Created 16/05/2021
Login API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import AuthDto
from app.main.service.user_service import find_user_by_username
from app.main.util.jwt import generate_jwt_keypair
from flask import request

api = AuthDto.api


@api.route("/login")
class Login(Resource):
    """ Resource for /auth/login """

    @api.doc("Login User")
    @api.response(200, "Successful Login")
    @api.response(401, "Login Failed")
    @api.expect(AuthDto.credentials, validate=True)
    def post(self):
        """
        POST /login
        Expected: AuthDto.credentials
        """
        user = find_user_by_username(request.json.get("username"))

        if user is None:
            return self.format_failure(401, "Login Failed")

        password_valid = user.verify_password(request.json.get("password"))
        if not password_valid:
            return self.format_failure(401, "Login Failed")

        access, refresh = generate_jwt_keypair(
            user.id, user.tribe_id, user.role)

        return self.format_success(200, {
            "user": user.dictionary,
            "tokens": {
                "access": access,
                "refresh": refresh
            }
        })

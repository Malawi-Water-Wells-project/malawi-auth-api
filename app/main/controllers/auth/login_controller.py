"""
Created 16/05/2021
Login API Resource
"""
from app.main.service.token_service import TokenService
from app.main.models.user import User
from app.main.controllers.resource import Resource
from app.main.dto import AuthDto
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
        username = request.json.get("username")
        password = request.json.get("password")

        try:
            user = User.get(username)
            if not user.verify_password(password):
                return self.format_failure(401, "Login Failed")

            access, refresh = TokenService.create_keypair(
                user_id=user.user_id,
                tribe_id=user.tribe_id,
                role=user.role
            )

            return self.format_success(200, {
                "user": user.dictionary,
                "tokens": {
                    "access": access,
                    "refresh": refresh
                }
            })

        except User.DoesNotExist:
            return self.format_failure(401, "Login Failed")

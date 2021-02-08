

from app.main.util.jwt import generate_jwt_keypair
from flask.globals import request
from app.main.service.user_service import find_user_by_username
from flask_restx.resource import Resource
from app.main.dto import AuthDto


api = AuthDto.api
_credentials = AuthDto.credentials


@api.route("/login")
class Login(Resource):
    @api.doc("Login")
    @api.response(200, "Logged in successfully")
    @api.response(401, "Login Failed")
    @api.expect(_credentials, validate=True)
    def post(self):
        user = find_user_by_username(request.json.get("username"))

        if user is None:
            return {
                "status": "Failure",
                "message": "Login Failed"
            }, 401

        password_valid = user.verify_password(request.json.get("password"))

        if password_valid is False:
            return {
                "status": "Failure",
                "message": "Login Failed"
            }, 401

        access_token, refresh_token = generate_jwt_keypair(
            user.id, user.tribe_id, user.role)

        return {
            "status": "Success",
            "user": user.to_object(),
            "tokens": {
                "access": access_token,
                "refresh": refresh_token
            }
        }

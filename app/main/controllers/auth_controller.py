

from app.main.service.token_service import get_refresh_token
import jwt
from app.main.util.decorator import user_logged_in
from app.main.util.jwt import generate_access_token, generate_jwt_keypair, validate_refresh_token
from flask.globals import request
from app.main.service.user_service import find_user_by_id, find_user_by_username
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


@api.route("/authorize")
class Authorize(Resource):
    @api.doc("Get new Access Token")
    @api.response(200, "Access Token Successfully Created")
    @api.response(401, "Invalid Refresh Token")
    def post(self):
        token = request.headers.get("Authorization")

        error, payload = validate_refresh_token(token)

        if "Bearer" in token:
            token = token.split(" ").pop()

        if error is not None:
            return {
                "status": "Failure",
                "message": "Invalid Token"
            }, 401

        existing_token = get_refresh_token(token)
        if existing_token == None:
            return {
                "status": "Failure",
                "message": "Invalid Token"
            }, 401

        if existing_token.revoked:
            return {
                "status": "Failure",
                "message": "Token Revoked"
            }, 401

        user = find_user_by_id(int(existing_token.user_id))
        if user is None:
            return {
                "status": "Failure",
                "message": "User Not Existing"
            }, 404

        new_access_token = generate_access_token(
            user.id, user.tribe_id, user.role)

        return {
            "status": "Success",
            "token": new_access_token
        }


@api.route("/user")
class User(Resource):
    @api.doc("Gets the current user")
    @api.response(200, "Current User")
    @api.response(401, "Not Logged In")
    @api.response(404, "User Not Found")
    @user_logged_in
    def get(self, jwt):
        user = find_user_by_id(jwt.get("user_id"))
        if user is None:
            return {
                "status": "Failure",
                "message": "User Not Found"
            }, 404

        return {
            "status": "Success",
            "user": user.to_object()
        }

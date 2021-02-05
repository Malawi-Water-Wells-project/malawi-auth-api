

from flask.globals import request
from app.main.service.user_service import find_user_by_username
from flask_restx.resource import Resource
from app.main.dto import AuthDto


api = AuthDto.api
_credentials = AuthDto.credentials

# /auth/login


@api.route("/login")
class Login(Resource):
    @api.doc("Login")
    @api.response(200, "Logged in successfully")
    @api.expect(_credentials, validate=True)
    def post(self):
        user = find_user_by_username(request.json["username"])

        if user is None:
            return 404

        return {
            "status": "Success",
            "user": user.to_object()
        }

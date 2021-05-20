"""
Created 15/05/2021
CreateUser API Resource
"""
from app.main.constants import UserRoles
from app.main.controllers.resource import Resource
from app.main.dto import UserDto
from app.main.service.user_service import create_new_user
from app.main.util.decorators.auth import AuthDecorators
from app.main.util.decorators.middleware import validate
from app.main.util.validation.requests import CreateUserValidator
from flask import request

api = UserDto.api


@api.route("/create")
class CreateUser(Resource):
    """ Resource for /users/create """

    @api.doc("Create a new User")
    @AuthDecorators.ensure_is_admin
    @validate(CreateUserValidator)
    def post(self):
        """
        POST /users/create
        """
        user = create_new_user(
            data=request.json,
            tribe_id=request.json.get("tribe_id", None),
            role=UserRoles.USER
        )

        return self.format_success(200, {"user": user.dictionary})

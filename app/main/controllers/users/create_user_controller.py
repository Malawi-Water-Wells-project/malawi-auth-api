"""
Created 15/05/2021
CreateUser API Resource
"""
from app.main.models.tribe import Tribe
from app.main.models.user import User
from app.main.constants import UserRoles
from app.main.controllers.resource import Resource
from app.main.dto import UserDto
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
    def post(self, tribe: Tribe, **_):
        """
        POST /users/create
        """
        role = request.json.get("role", UserRoles.USER)
        tribe_id = tribe.tribe_id if tribe is not None else None

        user = User(
            username=request.json["username"],
            name=request.json["name"],
            role=role,
            tribe_id=tribe_id
        )
        user.set_password(request.json["password"])
        user.save()

        assert user.user_id is not None

        if tribe:
            tribe.users.add(user.user_id)
            tribe.save()

        return self.format_success(201, {"user": user.dictionary})

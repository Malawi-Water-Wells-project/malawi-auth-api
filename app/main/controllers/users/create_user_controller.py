"""
Created 15/05/2021
CreateUser API Resource
"""
from app.main.models.village import Village
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
    def post(self, village: Village, **_):
        """
        POST /users/create
        """
        role = request.json.get("role", UserRoles.USER)
        village_id = village.village_id if village is not None else None

        user = User(
            username=request.json["username"],
            name=request.json["name"],
            role=role,
            village_id=village_id
        )
        user.set_password(request.json["password"])
        user.save()

        assert user.user_id is not None

        if village:
            village.users.add(user.user_id)
            village.save()

        return self.format_success(201, {"user": user.dictionary})

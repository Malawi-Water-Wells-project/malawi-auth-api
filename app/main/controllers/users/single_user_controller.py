"""
Created 15/05/2021
User API Resource
"""
from app.main.constants import UserRoles
from app.main.controllers.resource import Resource
from app.main.dto import UserDto
from app.main.models.user import User
from app.main.service.tribe_service import TribeService
from app.main.service.user_service import UserService
from app.main.util.decorators.auth import AuthDecorators
from app.main.util.decorators.middleware import validate
from app.main.util.validation.requests import PatchUserValidator
from flask import request

api = UserDto.api


@api.route("/<string:user_id>")
class UserResource(Resource):
    """ Resource for /user/<user_id> """

    def get(self, user_id: str):
        """
        GET /user/<user_id>
        Returns a User if found
        """
        user = UserService.get_by_public_id(user_id)

        if user is None:
            return self.format_failure(404, "User not found")

        return self.format_success(200, {"user": user.dictionary})

    @AuthDecorators.ensure_user_access
    @validate(PatchUserValidator)
    def patch(self, user: User, jwt: dict, **_):
        """
        PATCH /user/<user_id>
        Edits a User
        """
        user.name = request.json.get("name") or user.name
        user.username = request.json.get("username") or user.username

        tribe_id = request.json.get("tribe_id")
        if tribe_id is not None:
            tribe = TribeService.get_by_public_id(tribe_id)
            if tribe is None:
                return self.format_failure(404, "Tribe not found")
            user.tribe_id = tribe_id

        role = request.json.get("role")
        if role is not None:
            if jwt.get("role") != UserRoles.ADMIN:
                return self.format_failure(401, "You are not authorized to perform this action")
            user.role = role

        user.save()

        return self.format_success(200, {"user": user.dictionary})

    def delete(self, user_id: str):
        """
        DELETE /user/<user_id>
        Deletes a User
        """
        user = UserService.get_by_public_id(user_id)

        if user is None:
            return self.format_failure(404, "User not found")

        user.delete()

        return self.format_success(204)

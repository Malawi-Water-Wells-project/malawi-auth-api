"""
Created 16/05/2021
CurrentUser API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import UserDto
from app.main.service.user_service import UserService
from app.main.util.decorators.auth import AuthDecorators

api = UserDto.api


@api.route("/current")
class CurrentUser(Resource):
    """ CurrentUser API Resource """

    @AuthDecorators.ensure_logged_in
    def get(self, jwt: dict):
        """
        GET /users/current
        Returns the currently logged-in user
        """
        user_id = jwt.get("user_id")

        user = UserService.get_by_id(user_id)
        if user is None:
            return self.format_failure(500, "User Not Found")

        return self.format_success(200, {"user": user.dictionary})

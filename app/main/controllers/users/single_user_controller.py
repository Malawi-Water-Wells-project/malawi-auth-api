"""
Created 15/05/2021
User API Resource
"""
from app.main.service.token_service import TokenService
from app.main.service.village_service import VillageService
from pynamodb.exceptions import DeleteError
from app.main.service.user_service import UserService
from app.main.controllers.resource import Resource
from app.main.dto import UserDto

api = UserDto.api


@api.route("/<string:user_id>")
class UserResource(Resource):
    """ Resource for /user/<user_id> """

    def get(self, user_id: str):
        """
        GET /user/<user_id>
        Returns a User if found
        """
        user = UserService.get_by_id(user_id)

        if user is None:
            return self.format_failure(404, "User not found")

        return self.format_success(200, {"user": user.dictionary})

    def delete(self, user_id: str):
        """
        DELETE /user/<user_id>
        Deletes a User
        """
        user = UserService.get_by_id(user_id)
        if user is None:
            return self.format_failure(404, "User not found")

        # Revoke Refresh Tokens
        TokenService.remove_tokens_for_user(user_id)

        # Remove User from their Village
        if user.village_id is not None:
            village = VillageService.get_by_id(user.village_id)
            if village is not None:
                village.users.remove(user_id)
                village.save()

        # Delete the User
        try:
            user.delete()
            return self.format_success(204)
        except DeleteError:
            return self.format_failure(500, "Failed to delete user")

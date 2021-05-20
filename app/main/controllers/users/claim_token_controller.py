"""
Created 20/05/2021
ClaimToken API Resource
"""
from app.main.constants import UserRoles
from app.main.controllers.resource import Resource
from app.main.dto import UserDto
from app.main.models.tribe import Tribe
from app.main.service.user_service import create_new_user
from app.main.util.decorators.middleware import validate
from app.main.util.jwt import generate_jwt_keypair
from app.main.util.validation.requests import ClaimTokenValidator

api = UserDto.api


@api.route("/claim-token")
class ClaimToken(Resource):
    """ Resource for /users/claim-token """

    @api.doc("Creates a standard user associated with a tribe")
    @validate(ClaimTokenValidator)
    def post(self, body: dict, tribe: Tribe):
        """
        POST /users/claim-token
        Creates a standard user, using authorization from the token provided
        Also links the user with a tribe obtained from the token.
        """
        user = create_new_user(body, tribe.public_id, UserRoles.USER)

        access, refresh = generate_jwt_keypair(
            user.id, tribe.id, user.role)

        return self.format_success(200, {
            "user": user.dictionary,
            "tokens": {
                "access": access,
                "refresh": refresh
            }
        })

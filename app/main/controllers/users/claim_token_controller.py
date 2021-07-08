"""
Created 20/05/2021
ClaimToken API Resource
"""
from app.main.models.user import User
from app.main.constants import UserRoles
from app.main.controllers.resource import Resource
from app.main.dto import UserDto
from app.main.models.tribe import Tribe
from app.main.service.user_service import UserService
from app.main.util.decorators.middleware import validate
from app.main.util.jwt import generate_jwt_keypair
from app.main.util.validation.requests import ClaimTokenValidator

api = UserDto.api


@api.route("/claim-token")
class ClaimToken(Resource):
    """ Resource for /users/claim-token """

    @api.doc("Creates a standard user associated with a tribe")
    @validate(ClaimTokenValidator)
    def post(self, tribe: Tribe, body: dict, **_):
        """
        POST /users/claim-token
        Creates a standard user, using authorization from the token provided
        Also links the user with a tribe obtained from the token.
        """
        del body["token"]

        user = User.create(tribe_id=tribe.id,
                           role=UserRoles.USER, **body)

        print(user)
        access, refresh = generate_jwt_keypair(
            user.id, tribe.id, user.role)

        return self.format_success(200, {
            "user": user.dictionary,
            "tokens": {
                "access": access,
                "refresh": refresh
            }
        })

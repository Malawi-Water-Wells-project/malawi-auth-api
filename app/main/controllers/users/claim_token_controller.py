"""
Created 20/05/2021
ClaimToken API Resource
"""
from app.main.models.user import User
from app.main.constants import UserRoles
from app.main.controllers.resource import Resource
from app.main.dto import UserDto
from app.main.models.village import Village
from app.main.service.user_service import UserService
from app.main.util.decorators.middleware import validate
from app.main.util.jwt import generate_jwt_keypair
from app.main.util.validation.requests import ClaimTokenValidator

api = UserDto.api


@api.route("/claim-token")
class ClaimToken(Resource):
    """ Resource for /users/claim-token """

    @api.doc("Creates a standard user associated with a village")
    @validate(ClaimTokenValidator)
    def post(self, village: Village, body: dict, **_):
        """
        POST /users/claim-token
        Creates a standard user, using authorization from the token provided
        Also links the user with a village obtained from the token.
        """
        del body["token"]

        user = User.create(village_id=village.id,
                           role=UserRoles.USER, **body)

        print(user)
        access, refresh = generate_jwt_keypair(
            user.id, village.id, user.role)

        return self.format_success(200, {
            "user": user.dictionary,
            "tokens": {
                "access": access,
                "refresh": refresh
            }
        })

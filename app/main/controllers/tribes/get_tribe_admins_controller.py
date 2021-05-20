"""
Created 20/05/2021
GetTribeAdmins API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import TribeDto
from app.main.service.tribe_service import get_tribe_by_public_id

api = TribeDto.api


@api.route("/<string:tribe_id>/admins")
class GetTribeAdmins(Resource):
    """ Resource for /tribes/<tribe_id>/admins/ """

    @api.doc("Gets all the Tribe Admins in a Tribe")
    def get(self, tribe_id: str):
        """
        GET /tribes/<tribe_id>/admins
        Gets all Tribe Admins in a Tribe
        """

        tribe = get_tribe_by_public_id(tribe_id)

        if not tribe:
            return self.format_failure(404, "Tribe Not Found")

        admins = [admin.dictionary for admin in tribe.get_admins()]

        return self.format_success(200, {"admins": admins})

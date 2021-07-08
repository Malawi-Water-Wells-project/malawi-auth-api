"""
Created 20/05/2021
GetTribeAdmins API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import TribeDto
from app.main.service.tribe_service import TribeService

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

        tribe = TribeService.get_by_id(tribe_id)

        if not tribe:
            return self.format_failure(404, "Tribe Not Found")

        admins = TribeService.get_tribeadmins(tribe)

        return self.format_success(200, {"admins": [admin.dictionary for admin in admins]})

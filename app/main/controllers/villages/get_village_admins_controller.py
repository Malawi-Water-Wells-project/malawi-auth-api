"""
Created 20/05/2021
GetVillageAdmins API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import VillageDto
from app.main.service.village_service import VillageService

api = VillageDto.api


@api.route("/<string:village_id>/admins")
class GetVillageAdmins(Resource):
    """ Resource for /villages/<village_id>/admins/ """

    @api.doc("Gets all the Village Admins in a Village")
    def get(self, village_id: str):
        """
        GET /villages/<village_id>/admins
        Gets all Village Admins in a Village
        """

        village = VillageService.get_by_id(village_id)

        if not village:
            return self.format_failure(404, "Village Not Found")

        admins = VillageService.get_villageadmins(village)

        return self.format_success(200, {"admins": [admin.dictionary for admin in admins]})

"""
Created 15/05/2021
GetVillageByID API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import VillageDto
from app.main.service.village_service import VillageService

api = VillageDto.api


@api.route("/<string:village_id>")
class GetVillageByID(Resource):
    """
    API Resource for /villages/<village_id>/
    """

    @api.doc("Lookup a Village by Public ID")
    @api.response(200, "Village Found")
    @api.response(404, "Village Not Found")
    def get(self, village_id: str):
        """
        GET /villages/<village_id>
        Lookup a Village by Public ID
        """

        village = VillageService.get_by_id(village_id)

        if village is None:
            return self.format_failure(404, "Village Not Found")

        return self.format_success(200, {
            "village": village.dictionary
        })

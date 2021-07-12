"""
Created 19/05/2021
GetCurrentVillage API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import VillageDto
from app.main.service.village_service import VillageService
from app.main.util.decorators.auth import AuthDecorators

api = VillageDto.api


@api.route("/current")
class GetCurrentVillage(Resource):
    """ API Resource for /villages/current """

    @api.doc("Gets the Village associated with the logged-in user")
    @AuthDecorators.ensure_logged_in
    def get(self, jwt):
        """
        GET /villages/current
        Gets the Village for the currently logged in user
        """
        village_id = jwt.get("village_id")

        if not village_id:
            return self.format_failure(400, "You are not associated with a village")

        village = VillageService.get_by_id(village_id)
        if not village:
            return self.format_failure(404, "Village not found")

        return self.format_success(200, {"village": village.dictionary})

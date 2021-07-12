"""
Created 20/05/2021
GenerateVillageToken API Resource
"""

from app.main.controllers.resource import Resource
from app.main.dto import VillageDto
from app.main.models.village import Village
from app.main.service.village_service import VillageService
from app.main.util.decorators.auth import AuthDecorators

api = VillageDto.api


@api.route("/<string:village_id>/generate-token")
class GenerateVillageToken(Resource):
    """ Resource for /villages/<village_id>/generate-token """

    @api.doc("Creates a Join Token for a Village")
    @AuthDecorators.ensure_is_village_admin
    def get(self, village: Village, **_):
        """
        GET /villages/<village_id>/generate-token
        Creates a Join Token that can be standard users can use to join a village
        """
        token = VillageService.create_join_token(village)
        return self.format_success(200, {"token": token.token_id})

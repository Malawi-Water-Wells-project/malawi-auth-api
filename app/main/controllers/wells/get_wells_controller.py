"""
Created 19/05/2021
GetWells API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import WellDto
from app.main.service.well_service import get_all_wells
from app.main.util.decorator import AuthDecorators

api = WellDto.api


@api.route("/")
class Wells(Resource):
    """ API Resource for /wells/ """

    @api.doc("Retrieves all wells")
    @api.response(200, "An array of Well objects")
    @AuthDecorators.ensure_logged_in
    def get(self, **_):
        """
        GET /wells/

        Retrieves all wells that the user is allowed to see.
        """
        wells = [well.dictionary for well in get_all_wells()]

        return self.format_success(200, {"wells": wells})

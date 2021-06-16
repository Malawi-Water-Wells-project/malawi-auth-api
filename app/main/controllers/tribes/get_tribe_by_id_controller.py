"""
Created 15/05/2021
GetTribeByID API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import TribeDto
from app.main.service.tribe_service import TribeService

api = TribeDto.api


@api.route("/<string:tribe_id>")
class GetTribeByID(Resource):
    """
    API Resource for /tribes/<tribe_id>/
    """

    @api.doc("Lookup a Tribe by Public ID")
    @api.response(200, "Tribe Found")
    @api.response(404, "Tribe Not Found")
    def get(self, tribe_id):
        """
        GET /tribes/<tribe_id>
        Lookup a Tribe by Public ID
        """

        tribe = TribeService.get_by_id(tribe_id)

        if tribe is None:
            return self.format_failure(404, "Tribe Not Found")

        return self.format_success(200, {
            "tribe": tribe.dictionary
        })

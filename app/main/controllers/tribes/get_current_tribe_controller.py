"""
Created 19/05/2021
GetCurrentTribe API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import TribeDto
from app.main.service.tribe_service import get_tribe_by_id
from app.main.util.decorator import AuthDecorators

api = TribeDto.api


@api.route("/current")
class GetCurrentTribe(Resource):
    """ API Resource for /tribes/current """

    @api.doc("Gets the Tribe associated with the logged-in user")
    @AuthDecorators.ensure_logged_in
    def get(self, jwt):
        """
        GET /tribes/current
        Gets the Tribe for the currently logged in user
        """
        tribe_id = jwt.get("tribe_id")

        if not tribe_id:
            return self.format_failure(400, "This user is not associated with a tribe")

        tribe = get_tribe_by_id(tribe_id)
        if not tribe:
            return self.format_failure(404, "Tribe not found")

        return self.format_success(200, {tribe: tribe.dictionary})

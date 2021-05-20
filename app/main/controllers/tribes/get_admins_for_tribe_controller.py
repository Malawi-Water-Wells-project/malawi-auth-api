"""
Created 15/05/2021
GetAdminsForTribe API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import TribeDto
from app.main.service.tribe_service import save_new_tribe
from app.main.util.decorators.auth import AuthDecorators
from flask import request

api = TribeDto.api
_tribe = TribeDto.tribe


class GetAdminsForTribe(Resource):
    """ Resource for /tribes/create """

    @api.doc("Creates a new Tribe")
    @api.response(201, "Tribe Created")
    @api.expect(_tribe, validate=True)
    @AuthDecorators.ensure_is_admin
    def post(self):
        """
        POST /tribes/create
        Creates a new Tribe
        """
        new_tribe = save_new_tribe(request.json)
        return self.format_success(401, {"tribe": new_tribe.dictionary})

"""
Created 24/05/2021
CreateTribe API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import TribeDto
from app.main.service.tribe_service import save_new_tribe
from flask import request

api = TribeDto.api
_tribe = TribeDto.tribe


@api.route("/create")
class CreateTribe(Resource):
    """ Resource for /tribes/create """

    @api.doc("Create a new Tribe")
    @api.response(201, "Tribe created successfully")
    @api.expect(_tribe, validate=True)
    def post(self):
        """
        POST /tribes/create
        Creates a new Tribe
        """

        new_tribe = save_new_tribe(request.json)
        return self.format_success(201, {"tribe": new_tribe.dictionary})

"""
Created 24/05/2021
CreateTribe API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import TribeDto
from app.main.models.tribe import Tribe
from flask import request

api = TribeDto.api
_tribe = TribeDto.tribe


@api.route("/create")
class CreateTribe(Resource):
    """ Resource for /tribes/create """

    @api.doc("Create a new Tribe")
    @api.response(201, "Tribe created successfully")
    @api.expect(_tribe, validate=True)
    def post(self, **_):
        """
        POST /tribes/create
        Creates a new Tribe
        """
        tribe = Tribe(**request.json)
        tribe.save()
        return self.format_success(201, {"tribe": tribe.dictionary})

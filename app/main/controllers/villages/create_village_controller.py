"""
Created 24/05/2021
CreateVillage API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import VillageDto
from app.main.models.village import Village
from flask import request

api = VillageDto.api
_village = VillageDto.village


@api.route("/create")
class CreateVillage(Resource):
    """ Resource for /villages/create """

    @api.doc("Create a new village")
    @api.response(201, "Village created successfully")
    @api.expect(_village, validate=True)
    def post(self, **_):
        """
        POST /villages/create
        Creates a new Village
        """
        village = Village(**request.json)
        village.save()
        return self.format_success(201, {"village": village.dictionary})

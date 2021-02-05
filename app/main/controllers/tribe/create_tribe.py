from flask_restx import Resource
from app.main.dto import TribeDto

api = TribeDto.api


@api.route("/create")
class CreateTribe(Resource):
    @api.doc("Create a Tribe")
    def post(self):
        return "Hello"

from app.main.service.well_service import get_all_wells
from flask_restx.resource import Resource
from app.main.dto import WellDto
from app.main.util.decorator import user_logged_in
api = WellDto.api


@api.route("/")
class Wells(Resource):
    @api.doc("Retrieves Wells")
    @user_logged_in
    def get(self, jwt):
        wells = [well.to_object() for well in get_all_wells()]

        return wells

from app.main.constants import UserRoles
from app.main.service.user_service import create_new_user
from flask.globals import request
from app.main.service.tribe_service import get_tribe_by_public_id, save_new_tribe
from flask_restx import Resource
from app.main.dto import TribeDto

api = TribeDto.api
_tribe = TribeDto.tribe
_admin = TribeDto.admin


@api.route("/create")
class CreateTribe(Resource):
    @api.doc("Create a new Tribe")
    @api.response(201, "Tribe created successfully")
    @api.expect(_tribe, validate=True)
    def post(self):
        new_tribe = save_new_tribe(request.json)
        return {
            "status": "Success",
            "tribe": new_tribe.to_object()
        }, 201


@api.route("/<tribe_id>/admin")
class TribeAdmin(Resource):
    @api.doc("Create a new tribe admin")
    @api.response(201, "Tribe Admin added successfully")
    @api.response(404, "Tribe not found")
    @api.expect(_admin, validate=True)
    def post(self, tribe_id):
        tribe = get_tribe_by_public_id(tribe_id)
        if tribe is None:
            return {
                "status": "Failure",
                "message": "Tribe not found"
            }, 404

        new_user = create_new_user(
            request.json,
            tribe.id,
            UserRoles.TRIBE_ADMIN
        )

        return {
            "status": "Success",
            "user": new_user.to_object()
        }, 201
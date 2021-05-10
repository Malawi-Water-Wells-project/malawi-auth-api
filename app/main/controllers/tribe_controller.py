from app.main.models.user import User
from app.main.util.decorator import user_logged_in, user_is_tribe_admin
from app.main.constants import DistanceConversions, UserRoles
from app.main.service.user_service import create_new_user, find_user_by_username, get_admins_by_tribe
from flask.globals import request
from app.main.service.tribe_service import TribeSearchQuery, check_join_token, create_tribe_join_token, get_tribe_by_id, get_tribe_by_public_id, lookup_join_token, save_new_tribe
from app.main.util.jwt import generate_jwt_keypair
from flask_restx import Resource, reqparse
from app.main.dto import TribeDto
import base64
import json
from math import cos, radians

api = TribeDto.api
_tribe = TribeDto.tribe
_admin = TribeDto.admin
_new_user = TribeDto.new_user


@api.route("/")
class GetTribe(Resource):
    @api.doc("Gets the current tribe")
    @user_logged_in
    def get(self, jwt):
        tribe_id = jwt.get("tribe_id")
        tribe = get_tribe_by_id(tribe_id)

        return {
            "status": "Success",
            "tribe": tribe.to_object()
        }


@api.route("/<string:tribe_id>")
class GetTribeByID(Resource):
    @api.doc("Retrives a Tribe by its public ID")
    def get(self, tribe_id):
        tribe = get_tribe_by_public_id(tribe_id)

        if tribe is None:
            return {
                "status": "Failure"
            }, 404

        return {
            "status": "Success",
            "tribe": tribe.to_object()
        }


@api.route("/<string:tribe_id>/admins")
class GetAdminsForTribe(Resource):
    @api.doc("Gets all Tribe Admins for a tribe")
    def get(self, tribe_id):
        tribe = get_tribe_by_public_id(tribe_id)

        if not tribe:
            return {
                "status": "Failure",
                "message": "Tribe not found"
            }, 404

        admins = get_admins_by_tribe(tribe.id)

        return {
            "status": "Success",
            "admins": [x.to_object() for x in admins]
        }


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

        existing_user = find_user_by_username(request.json.get("username"))
        if existing_user is not None:
            return {
                "status": "Failure",
                "message": "Username is already taken"
            }, 400

        new_user = create_new_user(
            request.json,
            tribe.id,
            UserRoles.TRIBE_ADMIN
        )

        return {
            "status": "Success",
            "user": new_user.to_object()
        }, 201


@api.route("/check-token")
class CheckToken(Resource):
    def post(self):
        token = request.json["token"]

        if token is None:
            return {}, 500

        decoded_token = json.loads(base64.b64decode(
            token.encode("ascii")).decode("ascii"))

        is_valid = check_join_token(decoded_token)

        if not is_valid:
            return {}, 500

        return {
            "status": "Success",
            "isValid": True,
            "token": decoded_token
        }


@api.route("/join")
class JoinTribe(Resource):
    @api.doc("Creates a standard user associated with a tribe")
    @api.expect(_new_user, validate=True)
    def post(self):
        token = lookup_join_token(request.json["token"])

        if token is None:
            return {}, 400

        tribe = get_tribe_by_public_id(token.get("tribe_id"))
        if tribe is None:
            return {}, 400

        user = create_new_user(request.json, tribe.id, UserRoles.USER)

        access_token, refresh_token = generate_jwt_keypair(
            user.id, tribe.id, user.role)

        return {
            "status": "Success",
            "user": user.to_object(),
            "tokens": {
                "access": access_token,
                "refresh": refresh_token
            }
        }


@api.route("/<tribe_id>/token")
class TribeToken(Resource):
    @api.doc("Creates a new standard user")
    @user_logged_in
    @user_is_tribe_admin
    def get(self, jwt, tribe_id, tribe):
        token = create_tribe_join_token(tribe.public_id, tribe.name)

        return {
            "status": "Success",
            "token": str(base64.encodestring(json.dumps(token).encode()), "utf-8")
        }


@api.route("/search")
class TribeSearch(Resource):

    @api.doc("Searches for Tribes")
    def get(self):
        search_query = self._parse_request()

        results = search_query.run_query()

        return {
            "status": "Success",
            "count": len(results),
            "results": [result.to_object() for result in results]
        }

    def _parse_request(self):
        parser = reqparse.RequestParser()
        parser.add_argument("type", type=str, required=True,
                            help="Type is required", location="args")
        parser.add_argument("query", type=str, location="args")
        parser.add_argument("latitude", type=float, location="args")
        parser.add_argument("longitude", type=float, location="args")
        parser.add_argument("radius", type=int, location="args")

        args = parser.parse_args()

        search_type = args.get("type", None)

        if search_type not in ["name", "location"]:
            return

        if search_type == "location":
            return self._parse_location(args)

    def _parse_location(self, args):
        latitude = args.get("latitude", None)
        longitude = args.get("longitude", None)
        radius = args.get("radius", None)

        if not latitude or not longitude:
            return {}

        return TribeSearchQuery(
            TribeSearchQuery.LOCATION_TYPE,
            latitude=latitude,
            longitude=longitude,
            radius=radius
        )

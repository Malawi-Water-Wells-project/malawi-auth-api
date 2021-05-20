"""
Created 20/05/2021
TribeSearch API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import TribeDto
from app.main.service.tribe_service import TribeSearchQuery
from flask_restx import reqparse

api = TribeDto.api


class TribeSearch(Resource):
    """ Resource for /tribes/search """

    @api.doc("Searches for Tribes")
    def get(self):
        """
        GET /tribes/search/
        Query for Tribes
        """
        search_query = self._parse_request()

        results = search_query.run_query()

        return self.format_success(200, {
            "count": len(results),
            "results": [result.dictionary for result in results]
        })

    def _parse_request(self) -> TribeSearchQuery:
        """ Parser for the incoming request """
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
            return None

        if search_type == "location":
            return self._parse_location(args)

        return None

    def _parse_location(self, args) -> TribeSearchQuery:
        """ Parse the lat/long and radius from the arguments """
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

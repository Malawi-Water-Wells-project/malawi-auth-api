"""
Created 20/05/2021
WellHygiene API Resource
"""
from app.main.service.well_hygiene_service import WellHygieneService
from app.main.service.well_service import WellService
from app.main.controllers.resource import Resource
from app.main.dto import WellDto
from app.main.util.decorators.middleware import validate
# from app.main.util.validation.requests import Well

from app.main.util.decorators.auth import AuthDecorators

api = WellDto.api


@api.route("/<string:well_id>/hygiene")
class WellHygiene(Resource):
    """ API Resource for /wells/<well_id>/hygiene """

    def get(self, well_id, **_):
        """
        GET /wells/<well_id>/hygiene
        """
        well = WellService.get_by_well_id(well_id)

        if well is None:
            return self.format_failure(404, "Well Not Found")

        return self.format_success(200, {"well": well})

    # @validate()
    def post(self, well_id: str):
        """
        POST /wells/<well_id>/hygiene
        """

        well = WellService.get_by_well_id(well_id)

        if well is None:
            self.format_failure(404, "Well Not Found")

        return self.format_success(200, {"well": well.dictionary})
        # WellHygieneService.record_hygiene()


# @api.route("/hygiene")
# class GetWellHygiene(Resource):
#     """ API Resource for /wells/hygiene """

#     @api.doc("Retrieve Well Hygiene")
#     @AuthDecorators.ensure_is_admin
#     def get(self, **_):
#         # wells = [well.dictionary for well in get_all_wells_hygiene()]

#         return {}


# def upload_well_hygiene():

#     file = open(r"C:\Users\lucym\Documents\bgsdata\well-hygiene.csv")
#     raw_csv = file.read()

#     hygieneuploader = BulkWellHygieneUploader()

#     has_parsed = hygieneuploader.parse(raw_csv)
#     if not has_parsed:
#         return print("not parsed")

#     hygieneuploader.upload()

# upload_well_hygiene()

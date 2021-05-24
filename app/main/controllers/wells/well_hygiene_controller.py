"""
Created 20/05/2021
GetWellHygiene API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import WellDto

from app.main.util.decorators.auth import AuthDecorators

api = WellDto.api


@api.route("/hygiene")
class GetWellHygiene(Resource):
    """ API Resource for /wells/hygiene """

    @api.doc("Retrieve Well Hygiene")
    @AuthDecorators.ensure_is_admin
    def get(self, **_):
        # wells = [well.dictionary for well in get_all_wells_hygiene()]

        return {}


# def upload_well_hygiene():

#     file = open(r"C:\Users\lucym\Documents\bgsdata\well-hygiene.csv")
#     raw_csv = file.read()

#     hygieneuploader = BulkWellHygieneUploader()

#     has_parsed = hygieneuploader.parse(raw_csv)
#     if not has_parsed:
#         return print("not parsed")

#     hygieneuploader.upload()

# upload_well_hygiene()

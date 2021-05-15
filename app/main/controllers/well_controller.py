"""
Created 01/03/2021
API Resources for /wells
"""

from app.main.dto import WellDto
from app.main.service.well_service import BulkWellUploader, get_all_wells
from app.main.util.decorator import user_logged_in
from flask import request
from flask_restx.resource import Resource

api = WellDto.api


@api.route("/")
class Wells(Resource):
    """ API Resource for /wells/ """

    @api.doc("Retrieves Wells")
    @api.response(200, "An array of Well objects")
    @user_logged_in
    def get(self, _jwt):
        """
        GET /wells/

        Retrieves all wells that the user is allowed to see.
        """
        wells = [well.dictionary for well in get_all_wells()]

        return wells


@api.route("/bulk")
class BulkUploadWells(Resource):
    """ API Resource for /wells/bulk/ """

    @api.doc("Bulk Upload of Wells")
    @api.response(200, "Status: Success - All Wells in the uploaded document have been added")
    @api.response(200, "Status: Mixed - Some Wells in the uploaded document could not be added")
    @api.response(400, "Status: Failure - No Wells were added")
    def post(self):
        """
        POST /wells/bulk
        Handler for the bulk CSV Well upload
        """

        raw_csv = request.files['file'].read()
        uploader = BulkWellUploader()

        has_parsed = uploader.parse(raw_csv)
        if not has_parsed:
            return {
                "status": "Failure",
                "message": "CSV could not be parsed"
            }, 400

        uploader.upload()

        successes = [row.get("WP_ID") for row in uploader.successful_rows]
        failures = [row.get("WP_ID") for row in uploader.failed_rows]

        if len(failures) == 0:
            return {
                "status": "Success",
                "successful": successes,
                "failures": failures
            }, 200

        if len(successes) == 0:
            return {
                "status": "Failure",
                "successful": successes,
                "failures": failures
            }, 400

        return {
            "status": "Mixed",
            "successful": successes,
            "failures": failures
        }, 200

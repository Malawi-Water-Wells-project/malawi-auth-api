"""
Created 19/05/2021
BulkUploadWells API Resource
"""
from app.main.controllers.resource import Resource
from app.main.dto import WellDto
from app.main.service.well_service import BulkWellUploader
from flask import request

api = WellDto.api

@api.route("/bulk")
class BulkUploadWells(Resource):
    """ API Resource for /wells/bulk """

    @api.doc("CSV Upload of multiple Wells")
    @api.response(200, "Status: Success - All Wells in the uploaded document have been added")
    @api.response(200, "Status: Mixed - Some Wells in the uploaded document could not be added")
    @api.response(400, "Status: Failure - No Wells were added")
    def post(self):
        """
        POST /wells/bulk/
        Handler for the bulk CSV Well upload
        """

        raw_csv = request.files["file"].read()
        uploader = BulkWellUploader()

        has_parsed = uploader.parse(raw_csv)

        if not has_parsed:
            return self.format_failure(400, "CSV could not be parsed")

        uploader.upload()

        result = {
            "successful_uploads": [row.get("WP_ID") for row in uploader.successful_rows],
            "failed_uploads": [row.get("WP_ID") for row in uploader.failed_rows]
        }

        if len(uploader.failed_rows) == 0:
            return self.format_success(200, result)

        if len(uploader.successful_rows) == 0:
            return self.format_failure(400, "Failed to upload wells", result)

        return self.format_mixed(200, "Some data failed to upload", result)

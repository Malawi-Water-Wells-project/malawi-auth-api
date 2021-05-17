from flask import request
from app.main.service.well_service import get_all_wells, BulkWellUploader
from app.main.util.add_well_hygiene import get_all_well_hygiene, BulkWellHygieneUploader
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


@api.route("/bulk")
class BulkUploadWells(Resource):
    @api.doc("Bulk Upload of Wells")
    def post(self):
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

@api.route("/wellhygiene")
class getwellhygiene(Resource):
    @api.doc("Retrieve Well Hygiene")
    @user_logged_in
    def get(self):
        wells = [well.to_object() for well in get_all_well_hygiene()]

        return wells

def upload_well_hygiene():

    file = open(r"C:\Users\lucym\Documents\bgsdata\well-hygiene.csv")
    raw_csv = file.read()

    hygieneuploader = BulkWellHygieneUploader()

    has_parsed = hygieneuploader.parse(raw_csv)
    if not has_parsed:
        return print("not parsed")

    hygieneuploader.upload()

upload_well_hygiene()
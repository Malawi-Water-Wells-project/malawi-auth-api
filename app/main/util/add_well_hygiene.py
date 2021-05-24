"""
Created 17/05/2021
Bulk Well Hygiene Uploader
"""
import io
from csv import DictReader

from app.main.models import db
from app.main.models.well_hygiene import WellHygiene


def get_all_wells_hygiene():
    return WellHygiene.query.all()


class BulkWellHygieneUploaderKeys:
    VILLAGE = "village"
    TC_DRY = "tc_dry"
    TC_WET = "tc_wet"
    FC_DRY = "fc_dry"
    FC_WET = "fc_wet"
    TURBIDITY_DRY = "turbidity_dry"
    TURBIDITY_WET = "turbidity_wet"
    TDS_DRY = "tds_dry"
    TDS_WET = "tds_wet"
    ELECTRICAL_CONDUCTIVITY_DRY = "electrical_conductivity_dry"
    ELECTRICAL_CONDUCTIVITY_WET = "electrical_conductivity_wet"
    PH_DRY = "ph_dry"
    PH_WET = "ph_wet"
    TEMPERATURE_DRY = "temperature_dry"
    TEMPERATURE_WET = "temperature_wet"
    FLUORIDE_DRY = "fluoride_dry"
    FLUORIDE_WET = "fluoride_wet"
    SULPHATE_DRY = "sulphate_dry"
    SULPHATE_WET = "sulphate_wet"
    HARDNESS_DRY = "hardness_dry"
    HARDNESS_WET = "hardness_wet"
    NITRATE_DRY = "nitrate_dry"
    NITRATE_WET = "nitrate_wet"
    AMMONIA_DRY = "ammonia_dry"
    AMMONIA_WET = "ammonia_wet"
    ARSONIC_DRY = "arsonic_dry"
    ARSONIC_WET = "arsonic_wet"
    NITRATENO2_DRY = "nitrateno2_dry"
    NITRATE_NO2_WET = "nitrate_no2_wet"
    TIMESTAMP = "timestamp"


class BulkWellHygieneUploader:

    EXPECTED_KEYS = (
        BulkWellHygieneUploaderKeys.VILLAGE,
        BulkWellHygieneUploaderKeys.TC_DRY,
        BulkWellHygieneUploaderKeys.TC_WET,
        BulkWellHygieneUploaderKeys.FC_DRY,
        BulkWellHygieneUploaderKeys.FC_WET,
        BulkWellHygieneUploaderKeys.TURBIDITY_DRY,
        BulkWellHygieneUploaderKeys.TURBIDITY_WET,
        BulkWellHygieneUploaderKeys.TDS_DRY,
        BulkWellHygieneUploaderKeys.TDS_WET,
        BulkWellHygieneUploaderKeys.ELECTRICAL_CONDUCTIVITY_DRY,
        BulkWellHygieneUploaderKeys.ELECTRICAL_CONDUCTIVITY_WET,
        BulkWellHygieneUploaderKeys.PH_DRY,
        BulkWellHygieneUploaderKeys.PH_WET,
        BulkWellHygieneUploaderKeys.TEMPERATURE_DRY,
        BulkWellHygieneUploaderKeys.TEMPERATURE_WET,
        BulkWellHygieneUploaderKeys.FLUORIDE_DRY,
        BulkWellHygieneUploaderKeys.FLUORIDE_WET,
        BulkWellHygieneUploaderKeys.SULPHATE_DRY,
        BulkWellHygieneUploaderKeys.SULPHATE_WET,
        BulkWellHygieneUploaderKeys.HARDNESS_DRY,
        BulkWellHygieneUploaderKeys.HARDNESS_WET,
        BulkWellHygieneUploaderKeys.NITRATE_DRY,
        BulkWellHygieneUploaderKeys.NITRATE_WET,
        BulkWellHygieneUploaderKeys.AMMONIA_DRY,
        BulkWellHygieneUploaderKeys.AMMONIA_WET,
        BulkWellHygieneUploaderKeys.ARSONIC_DRY,
        BulkWellHygieneUploaderKeys.ARSONIC_WET,
        BulkWellHygieneUploaderKeys.NITRATENO2_DRY,
        BulkWellHygieneUploaderKeys.NITRATE_NO2_WET,
        BulkWellHygieneUploaderKeys.TIMESTAMP,
    )

    def __init__(self):
        self.successful_rows = []
        self.failed_rows = []

    def parse(self, raw_data):
        try:
            io_stream = io.StringIO(raw_data)
            self.reader = DictReader(io_stream)
            return True
        except Exception as exc:
            print(exc)
            return False

    def upload(self):
        for row in self.reader:
            try:
                is_valid = self._validate_row(row)
                if not is_valid:
                    self.failed_rows.append(row)
                    continue

                well_hygiene = WellHygiene(
                    village=row.get(BulkWellHygieneUploaderKeys.VILLAGE, None),
                    tc_dry=row.get(BulkWellHygieneUploaderKeys.TC_DRY, None),
                    tc_wet=row.get(BulkWellHygieneUploaderKeys.TC_WET, None),
                    fc_dry=row.get(BulkWellHygieneUploaderKeys.FC_DRY, None),
                    fc_wet=row.get(BulkWellHygieneUploaderKeys.FC_WET, None),
                    turbidity_dry=row.get(BulkWellHygieneUploaderKeys.TURBIDITY_DRY, None),
                    turbidity_wet=row.get(BulkWellHygieneUploaderKeys.TURBIDITY_WET, None),
                    tds_dry=row.get(BulkWellHygieneUploaderKeys.TDS_DRY, None),
                    tds_wet=row.get(BulkWellHygieneUploaderKeys.TDS_WET, None),
                    electrical_conductivity_dry=row.get(BulkWellHygieneUploaderKeys.ELECTRICAL_CONDUCTIVITY_DRY, None),
                    electrical_conductivity_wet=row.get(BulkWellHygieneUploaderKeys.ELECTRICAL_CONDUCTIVITY_WET, None),
                    ph_dry=row.get(BulkWellHygieneUploaderKeys.PH_DRY, None),
                    ph_wet=row.get(BulkWellHygieneUploaderKeys.PH_WET, None),
                    temperature_dry=row.get(BulkWellHygieneUploaderKeys.TEMPERATURE_DRY, None),
                    temperature_wet=row.get(BulkWellHygieneUploaderKeys.TEMPERATURE_WET, None),
                    fluoride_dry=row.get(BulkWellHygieneUploaderKeys.FLUORIDE_DRY, None),
                    fluoride_wet=row.get(BulkWellHygieneUploaderKeys.FLUORIDE_WET, None),
                    sulphate_dry=row.get(BulkWellHygieneUploaderKeys.SULPHATE_DRY, None),
                    sulphate_wet=row.get(BulkWellHygieneUploaderKeys.SULPHATE_WET, None),
                    hardness_dry=row.get(BulkWellHygieneUploaderKeys.HARDNESS_DRY, None),
                    hardness_wet=row.get(BulkWellHygieneUploaderKeys.HARDNESS_WET, None),
                    nitrate_dry=row.get(BulkWellHygieneUploaderKeys.NITRATE_DRY, None),
                    nitrate_wet=row.get(BulkWellHygieneUploaderKeys.NITRATE_WET, None),
                    ammonia_dry=row.get(BulkWellHygieneUploaderKeys.AMMONIA_DRY, None),
                    ammonia_wet=row.get(BulkWellHygieneUploaderKeys.AMMONIA_WET, None),
                    arsonic_dry=row.get(BulkWellHygieneUploaderKeys.ARSONIC_DRY, None),
                    arsonic_wet=row.get(BulkWellHygieneUploaderKeys.ARSONIC_WET, None),
                    nitrateno2_dry=row.get(BulkWellHygieneUploaderKeys.NITRATENO2_DRY, None),
                    nitrate_no2_wet=row.get(BulkWellHygieneUploaderKeys.NITRATE_NO2_WET, None),
                    timestamp=row.get(BulkWellHygieneUploaderKeys.TIMESTAMP, None),
                )

                db.session.add(well_hygiene)
                db.session.commit()
                self.successful_rows.append(row)
            except Exception as exc:
                print(exc)
                self.failed_rows.append(row)

    def _validate_row(self, row):
        all_keys = list(row.keys())
        is_valid = True

        for key in self.EXPECTED_KEYS:
            if key not in all_keys:
                is_valid = False
                break

        return is_valid

    # def validate_bulk_upload(self, raw_csv):
    #     """
    #     Ensure that all required keys exist in the row
    #     """
    #     rows = DictReader(io.StringIO(raw_csv.decode("utf-8")))

    #     for row in rows:
    #         is_valid = validate_row()

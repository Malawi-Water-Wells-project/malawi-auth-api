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
    village = "village"
    tc_dry = "tc_dry"
    tc_wet = "tc_wet"
    fc_dry = "fc_dry"
    fc_wet = "fc_wet"
    turbidity_dry = "turbidity_dry"
    turbidity_wet = "turbidity_wet"
    tds_dry = "tds_dry"
    tds_wet = "tds_wet"
    electrical_conductivity_dry = "electrical_conductivity_dry"
    electrical_conductivity_wet = "electrical_conductivity_wet"
    ph_dry = "ph_dry"
    ph_wet = "ph_wet"
    temperature_dry = "temperature_dry"
    temperature_wet = "temperature_wet"
    fluoride_dry = "fluoride_dry"
    fluoride_wet = "fluoride_wet"
    sulphate_dry = "sulphate_dry"
    sulphate_wet = "sulphate_wet"
    hardness_dry = "hardness_dry"
    hardness_wet = "hardness_wet"
    nitrate_dry = "nitrate_dry"
    nitrate_wet = "nitrate_wet"
    ammonia_dry = "ammonia_dry"
    ammonia_wet = "ammonia_wet"
    arsonic_dry = "arsonic_dry"
    arsonic_wet = "arsonic_wet"
    nitrateno2_dry = "nitrateno2_dry"
    nitrate_no2_wet = "nitrate_no2_wet"
    timestamp = "timestamp"


class BulkWellHygieneUploader:

    EXPECTED_KEYS = (
        BulkWellHygieneUploaderKeys.village,
        BulkWellHygieneUploaderKeys.tc_dry,
        BulkWellHygieneUploaderKeys.tc_wet,
        BulkWellHygieneUploaderKeys.fc_dry,
        BulkWellHygieneUploaderKeys.fc_wet,
        BulkWellHygieneUploaderKeys.turbidity_dry,
        BulkWellHygieneUploaderKeys.turbidity_wet,
        BulkWellHygieneUploaderKeys.tds_dry,
        BulkWellHygieneUploaderKeys.tds_wet,
        BulkWellHygieneUploaderKeys.electrical_conductivity_dry,
        BulkWellHygieneUploaderKeys.electrical_conductivity_wet,
        BulkWellHygieneUploaderKeys.ph_dry,
        BulkWellHygieneUploaderKeys.ph_wet,
        BulkWellHygieneUploaderKeys.temperature_dry,
        BulkWellHygieneUploaderKeys.temperature_wet,
        BulkWellHygieneUploaderKeys.fluoride_dry,
        BulkWellHygieneUploaderKeys.fluoride_wet,
        BulkWellHygieneUploaderKeys.sulphate_dry,
        BulkWellHygieneUploaderKeys.sulphate_wet,
        BulkWellHygieneUploaderKeys.hardness_dry,
        BulkWellHygieneUploaderKeys.hardness_wet,
        BulkWellHygieneUploaderKeys.nitrate_dry,
        BulkWellHygieneUploaderKeys.nitrate_wet,
        BulkWellHygieneUploaderKeys.ammonia_dry,
        BulkWellHygieneUploaderKeys.ammonia_wet,
        BulkWellHygieneUploaderKeys.arsonic_dry,
        BulkWellHygieneUploaderKeys.arsonic_wet,
        BulkWellHygieneUploaderKeys.nitrateno2_dry,
        BulkWellHygieneUploaderKeys.nitrate_no2_wet,
        BulkWellHygieneUploaderKeys.timestamp,
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
                    village=row.get(BulkWellHygieneUploaderKeys.village, None),
                    tc_dry=row.get(BulkWellHygieneUploaderKeys.tc_dry, None),
                    tc_wet=row.get(BulkWellHygieneUploaderKeys.tc_wet, None),
                    fc_dry=row.get(BulkWellHygieneUploaderKeys.fc_dry, None),
                    fc_wet=row.get(BulkWellHygieneUploaderKeys.fc_wet, None),
                    turbidity_dry=row.get(
                        BulkWellHygieneUploaderKeys.turbidity_dry, None),
                    turbidity_wet=row.get(
                        BulkWellHygieneUploaderKeys.turbidity_wet, None),
                    tds_dry=row.get(BulkWellHygieneUploaderKeys.tds_dry, None),
                    tds_wet=row.get(BulkWellHygieneUploaderKeys.tds_wet, None),
                    electrical_conductivity_dry=row.get(
                        BulkWellHygieneUploaderKeys.electrical_conductivity_dry, None),
                    electrical_conductivity_wet=row.get(
                        BulkWellHygieneUploaderKeys.electrical_conductivity_wet, None),
                    ph_dry=row.get(BulkWellHygieneUploaderKeys.ph_dry, None),
                    ph_wet=row.get(BulkWellHygieneUploaderKeys.ph_wet, None),
                    temperature_dry=row.get(
                        BulkWellHygieneUploaderKeys.temperature_dry, None),
                    temperature_wet=row.get(
                        BulkWellHygieneUploaderKeys.temperature_wet, None),
                    fluoride_dry=row.get(
                        BulkWellHygieneUploaderKeys.fluoride_dry, None),
                    fluoride_wet=row.get(
                        BulkWellHygieneUploaderKeys.fluoride_wet, None),
                    sulphate_dry=row.get(
                        BulkWellHygieneUploaderKeys.sulphate_dry, None),
                    sulphate_wet=row.get(
                        BulkWellHygieneUploaderKeys.sulphate_wet, None),
                    hardness_dry=row.get(
                        BulkWellHygieneUploaderKeys.hardness_dry, None),
                    hardness_wet=row.get(
                        BulkWellHygieneUploaderKeys.hardness_wet, None),
                    nitrate_dry=row.get(
                        BulkWellHygieneUploaderKeys.nitrate_dry, None),
                    nitrate_wet=row.get(
                        BulkWellHygieneUploaderKeys.nitrate_wet, None),
                    ammonia_dry=row.get(
                        BulkWellHygieneUploaderKeys.ammonia_dry, None),
                    ammonia_wet=row.get(
                        BulkWellHygieneUploaderKeys.ammonia_wet, None),
                    arsonic_dry=row.get(
                        BulkWellHygieneUploaderKeys.arsonic_dry, None),
                    arsonic_wet=row.get(
                        BulkWellHygieneUploaderKeys.arsonic_wet, None),
                    nitrateno2_dry=row.get(
                        BulkWellHygieneUploaderKeys.nitrateno2_dry, None),
                    nitrate_no2_wet=row.get(
                        BulkWellHygieneUploaderKeys.nitrate_no2_wet, None),
                    timestamp=row.get(
                        BulkWellHygieneUploaderKeys.timestamp, None),
                )

                db.session.add(well_hygiene)
                db.session.commit()
                self.successful_rows.append(row)
            except:
                self.failed_rows.append(row)

    def _validate_row(self, row):
        all_keys = list(row.keys())
        is_valid = True

        for key in self.EXPECTED_KEYS:
            if key not in all_keys:
                is_valid = False
                break

        return is_valid

    def validate_bulk_upload(raw_csv):
        rows = DictReader(io.StringIO(raw_csv.decode("utf-8")))

        for row in rows:
            is_valid = validate_bulk_row()

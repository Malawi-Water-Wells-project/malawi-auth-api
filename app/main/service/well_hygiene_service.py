"""
Created 20/05/2021
DB Access Service for Well Hygiene
"""
from app.main.service.abstract_service import AbstractRedisService, AbstractService
import io
from csv import DictReader

from app.main.models import db
from app.main.models.well_hygiene import WellHygiene
import json


class WellHygieneService(AbstractRedisService):
    REDIS_DB = 1

    @classmethod
    def record_hygiene(cls, well_id: str, well_hygiene: WellHygiene):
        """ Saves Well Hygiene into Redis and stores the value in Postgres """
        response = cls.redisClient.set(cls._format_key(
            well_id), json.dumps(well_hygiene.dictionary))
        print(response)

    @classmethod
    def _format_key(cls, key: str) -> str:
        return f"wellhygiene:{key}"


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
    NO2_DRY = "nitrateno2_dry"
    NO2_WET = "nitrate_no2_wet"
    TIMESTAMP = "timestamp"


class BulkWellHygieneUploader:
    KEYS = BulkWellHygieneUploaderKeys
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
        BulkWellHygieneUploaderKeys.NO2_DRY,
        BulkWellHygieneUploaderKeys.NO2_WET,
        BulkWellHygieneUploaderKeys.TIMESTAMP
    )

    def __init__(self) -> None:
        self.successful_rows = []
        self.failed_rows = []
        self.reader = None

    def parse(self, raw_data):
        """ Attempt to parse the file into a CSV reader """
        try:
            io_stream = io.StringIO(raw_data)
            self.reader = DictReader(io_stream)
            return True
        except Exception as exc:
            print(exc)
            return False

    def upload(self):
        """ Upload each record """
        for row in self.reader:
            try:
                is_valid = self._validate_row(row)
                if not is_valid:
                    self.failed_rows.append(row)
                    continue

                model = self._create_model(row)
                db.session.add(model)
                db.session.commit()
                self.successful_rows.append(row)
            except Exception:  # pylint: disable=broad-except
                self.failed_rows.append(row)

    def _create_model(self, row: dict):
        """ Creates a WellHygiene Model from the row """
        return WellHygiene(
            village=row.get(self.KEYS.VILLAGE),
            tc_dry=row.get(self.KEYS.TC_DRY),
            tc_wet=row.get(self.KEYS.TC_WET),
            fc_dry=row.get(self.KEYS.FC_DRY),
            fc_wet=row.get(self.KEYS.FC_WET),
            turbidity_dry=row.get(self.KEYS.TURBIDITY_DRY),
            turbidity_wet=row.get(self.KEYS.TURBIDITY_WET),
            tds_dry=row.get(self.KEYS.TDS_DRY),
            tds_wet=row.get(self.KEYS.TDS_WET),
            electrical_conductivity_dry=row.get(
                self.KEYS.ELECTRICAL_CONDUCTIVITY_DRY),
            electrical_conductivity_wet=row.get(
                self.KEYS.ELECTRICAL_CONDUCTIVITY_WET),
            ph_dry=row.get(self.KEYS.PH_DRY),
            ph_wet=row.get(self.KEYS.PH_WET),
            temperature_dry=row.get(self.KEYS.TEMPERATURE_DRY),
            temperature_wet=row.get(self.KEYS.TEMPERATURE_WET),
            fluoride_dry=row.get(self.KEYS.FLUORIDE_DRY),
            fluoride_wet=row.get(self.KEYS.FLUORIDE_WET),
            sulphate_dry=row.get(self.KEYS.SULPHATE_DRY),
            sulphate_wet=row.get(self.KEYS.SULPHATE_WET),
            hardness_dry=row.get(self.KEYS.HARDNESS_DRY),
            hardness_wet=row.get(self.KEYS.HARDNESS_WET),
            nitrate_dry=row.get(self.KEYS.NITRATE_DRY),
            nitrate_wet=row.get(self.KEYS.NITRATE_WET),
            ammonia_dry=row.get(self.KEYS.AMMONIA_DRY),
            ammonia_wet=row.get(self.KEYS.AMMONIA_WET),
            arsonic_dry=row.get(self.KEYS.ARSONIC_DRY),
            arsonic_wet=row.get(self.KEYS.ARSONIC_WET),
            nitrateno2_dry=row.get(self.KEYS.NO2_DRY),
            nitrate_no2_wet=row.get(self.KEYS.NITRATE_WET),
            timestamp=row.get(self.KEYS.TIMESTAMP),
        )

    def _validate_row(self, row: dict):
        """ Validates  """
        all_keys = list(row.keys())
        for key in self.EXPECTED_KEYS:
            if key not in all_keys:
                return False
        return True

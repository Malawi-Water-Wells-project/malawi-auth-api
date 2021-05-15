"""
Created 01/03/2021
DB Access Service for Wells
"""
from csv import DictReader
from io import StringIO
from typing import List

from app.main.models import db
from app.main.models.well import Well


def get_all_wells() -> List[Well]:
    """ Returns every Well in the database - CAUTION! """
    return Well.query.all()


class BulkWellUploaderKeys:
    """ Required Keys in each row of the bulk CSV upload """
    WELL_ID = "WP_ID"
    COUNTRY = "Country"
    DISTRICT = "District"
    SUBDISTRICT = "SubDistrict"
    VILLAGE = "Village"
    LATITUDE = "Easting"
    LONGITUDE = "Northing"


class BulkWellUploader:
    """
    Handler for the Bulk Upload of Wells
    """

    EXPECTED_KEYS = (
        BulkWellUploaderKeys.WELL_ID,
        BulkWellUploaderKeys.COUNTRY,
        BulkWellUploaderKeys.DISTRICT,
        BulkWellUploaderKeys.SUBDISTRICT,
        BulkWellUploaderKeys.VILLAGE,
        BulkWellUploaderKeys.LATITUDE,
        BulkWellUploaderKeys.LONGITUDE
    )

    def __init__(self):
        self.successful_rows = []
        self.failed_rows = []
        self.reader = None

    def parse(self, raw_data) -> bool:
        """ Attempt to parse the incoming raw data into an IO stream """
        try:
            io_stream = StringIO(raw_data.decode())
            self.reader = DictReader(io_stream)
            return True
        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
            return False

    def upload(self) -> None:
        """ Creates a Well for each row in the uploaded CSV """
        for row in self.reader:
            success = self._upload_row(row)
            if success:
                self.successful_rows.append(row)
            else:
                self.failed_rows.append(row)

    def _upload_row(self, row: dict) -> bool:
        """ Attempt to validate and upload a single Well to the DB """
        is_valid = self._validate_row(row)
        if not is_valid:
            return False

        try:
            well = Well(
                well_id=row.get(BulkWellUploaderKeys.WELL_ID, None),
                country=row.get(BulkWellUploaderKeys.COUNTRY, None),
                district=row.get(BulkWellUploaderKeys.DISTRICT, None),
                sub_district=row.get(BulkWellUploaderKeys.SUBDISTRICT, None),
                village=row.get(BulkWellUploaderKeys.VILLAGE, None),
                latitude=row.get(BulkWellUploaderKeys.LATITUDE, None),
                longitude=row.get(BulkWellUploaderKeys.LONGITUDE, None)
            )
            db.session.add(well)
            db.session.commit()
            return True
        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
            return False

    def _validate_row(self, row: dict) -> bool:
        """
        Ensure that all required keys exist in the row
        """
        all_keys = list(row.keys())
        is_valid = True

        for key in self.EXPECTED_KEYS:
            if key not in all_keys:
                is_valid = False
                break

        return is_valid

from app.main.models.well import Well
from csv import DictReader
import io
from .. import db


def get_all_wells():
    return Well.query.all()


class BulkWellUploaderKeys:
    WELL_ID = "WP_ID"
    COUNTRY = "Country"
    DISTRICT = "District"
    SUBDISTRICT = "SubDistrict"
    VILLAGE = "Village"
    LATITUDE = "Easting"
    LONGITUDE = "Northing"


class BulkWellUploader:

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

    def parse(self, raw_data):
        try:
            io_stream = io.StringIO(raw_data.decode())
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

                well = Well(
                    well_id=row.get(BulkWellUploaderKeys.WELL_ID, None),
                    country=row.get(BulkWellUploaderKeys.COUNTRY, None),
                    district=row.get(BulkWellUploaderKeys.DISTRICT, None),
                    sub_district=row.get(
                        BulkWellUploaderKeys.SUBDISTRICT, None),
                    village=row.get(BulkWellUploaderKeys.VILLAGE, None),
                    latitude=row.get(BulkWellUploaderKeys.LATITUDE, None),
                    longitude=row.get(BulkWellUploaderKeys.LONGITUDE, None)
                )
                db.session.add(well)
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

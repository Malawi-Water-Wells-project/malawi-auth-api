"""
Created 01/03/2021
SQLAlchemy Model for a Well
"""
from uuid import uuid4
from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model


class Well(Model):
    """
    DynamoDB Model for a Well
    well_id: str        # UUID4, Hash Key, Public ID
    code: str           # Well's Code, i.e. AAA01
    country: str        # Well's Country
    district: str       # Well's District
    sub_district: str   # Well's Sub-District
    village: str        # Well's Village
    latitude: float     # Latitude of the well
    longitude: float    # Longitude of the well
    """
    class Meta:
        """ Metadata for Well Table """
        table_name = "dynamodb-well"
        host = "http://localhost:8000"
        read_capacity_units = 1
        write_capacity_units = 1

    well_id: str = UnicodeAttribute(
        hash_key=True,
        default=uuid4
    )
    code: str = UnicodeAttribute(range_key=True, null=False)
    country: str = UnicodeAttribute(null=False)
    district: str = UnicodeAttribute(null=False)
    sub_district: str = UnicodeAttribute(null=False)
    village: str = UnicodeAttribute(null=False)
    latitude: str = UnicodeAttribute(null=False)
    longitude: str = UnicodeAttribute(null=False)

"""
Created 05/02/2021
DynamoDB Model for a Village
"""

from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import (
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
    UnicodeSetAttribute
)
from uuid import uuid4
from typing import Set
from app.main.config import Config


class Village(Model):
    """
    DynamoDB Model for a Village

    village_id: str         # UUID4, Hash Key, Public ID
    name: str               # Village's name
    latitude: float         # Village's latitude
    longitude: float        # Village's longitude
    created_on: datetime    # Creation timestamp
    users: Set[str]         # List of User IDs
    wells: Set[str]         # List of Well IDs
    """

    class Meta:
        """ Metadata for Villages Table """
        table_name = Config.Tables.VILLAGES
        region = Config.AWS_REGION

    village_id: str = UnicodeAttribute(
        hash_key=True,
        default=lambda: str(uuid4())
    )
    name: str = UnicodeAttribute(null=False)
    latitude: float = NumberAttribute(null=False)
    longitude: float = NumberAttribute(null=False)
    created_on: datetime = UTCDateTimeAttribute(default=datetime.now)
    users: Set[str] = UnicodeSetAttribute(default=[])
    wells: Set[str] = UnicodeSetAttribute(default=[])

    def __repr__(self):
        return "<Village " + \
            f"village_id='{self.village_id}' " + \
            f"name='{self.name}' " + \
            f"latitude={self.latitude} " + \
            f"longitude={self.longitude} " + \
            f"created_on='{self.created_on}' " + \
            f"users={self.users} " + \
            f"wells={self.wells}>"

    @property
    def dictionary(self):
        """ A representation of the Village as a dict """
        values = self.attribute_values.copy()
        values["created_on"] = values["created_on"].isoformat()
        values["users"] = list(values["users"])
        values["wells"] = list(values["wells"])
        return values

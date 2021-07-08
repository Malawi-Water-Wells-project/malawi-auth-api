"""
Created 05/02/2021
DynamoDB Model for a Tribe
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
from typing import List, Set


class Tribe(Model):
    """
    DynamoDB Model for a Tribe

    tribe_id: str           # UUID4, Hash Key, Public ID
    name: str               # Tribe's name
    latitude: float         # Tribe's latitude
    longitude: float        # Tribe's longitude
    created_on: datetime    # Creation timestamp
    users: List[str]        # List of User IDs
    wells: List[str]        # List of Well IDs
    """

    class Meta:
        """ Metadata for Tribe Table """
        table_name = "dynamodb-tribe"
        read_capacity_units = 1
        write_capacity_units = 1

    tribe_id: str = UnicodeAttribute(
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
        return "<Tribe " + \
            f"tribe_id='{self.tribe_id}' " + \
            f"name='{self.name}' " + \
            f"latitude={self.latitude} " + \
            f"longitude={self.longitude} " + \
            f"created_on='{self.created_on}' " + \
            f"users={self.users} " + \
            f"wells={self.wells}>"

    @property
    def dictionary(self):
        """ A representation of the Tribe as a dict """
        values = self.attribute_values.copy()
        values["created_on"] = values["created_on"].isoformat()
        values["users"] = list(values["users"])
        values["wells"] = list(values["wells"])
        return values

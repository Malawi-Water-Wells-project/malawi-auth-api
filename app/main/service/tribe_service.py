"""
Created 05/02/2021
DB Access Service for Tribes
"""

import json
from datetime import datetime
from math import cos, radians, sqrt
from typing import List, Union
from uuid import uuid4

import redis
from app.main.constants import DistanceConversions
from app.main.models import db
from app.main.models.tribe import Tribe

# TODO: Proper Redis Config
r = redis.Redis(host="localhost", port=6379, db=0)


def save_new_tribe(data: dict) -> Tribe:
    """
    Creates a new Tribe in the DB
    """
    new_tribe = Tribe(
        public_id=str(uuid4()),
        name=data.get("name"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        created_on=datetime.utcnow()
    )
    db.session.add(new_tribe)
    db.session.commit()

    return new_tribe


def get_tribe_by_public_id(tribe_id) -> Union[Tribe, None]:
    """ Queries for Tribes by Public ID """
    return Tribe.query.filter_by(public_id=tribe_id).first()


def get_tribe_by_id(tribe_id) -> Union[Tribe, None]:
    """ Queries for Tribes by ID """
    return Tribe.query.filter_by(id=tribe_id).first()


def create_tribe_join_token(tribe_id: str, tribe_name: str) -> dict:
    """ Creates a token that can be used to join a Tribe """
    token = str(uuid4())

    token_data = {
        "token": token,
        "tribe_id": tribe_id,
        "tribe_name": tribe_name
    }

    success = r.setex(f"jointoken:{token}", 15 * 60, json.dumps(token_data))

    if success:
        return token_data

    raise Exception("Failed to set jointoken")


def check_join_token(token) -> bool:
    """ Validates a Join Token """
    if "token" in token:
        data = r.get(f"jointoken:{token.get('token')}")
        print(data)
        return True

    raise Exception("Oops!")


def lookup_join_token(token):
    """ Queries Redis for a Join Token """
    response = r.get(f"jointoken:{token}")

    if response is None:
        return None

    return json.loads(response)


class TribeSearchQuery:
    """
    Handler for Tribe Searches
    Implements a fuzzy-match name search (TODO) and a location-based search
    """
    LOCATION_TYPE = "location"
    NAME_TYPE = "name"

    def __init__(
        self,
        search_type: str = None,
        latitude: float = None,
        longitude: float = None,
        radius: int = None,
        name: str = None
    ):
        self.type = search_type
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.name = name

    def run_query(self) -> List[Tribe]:
        """ Runs the configured query """
        if self.type == self.LOCATION_TYPE:
            return self._run_location_query()
        if self.type == self.NAME_TYPE:
            return self._run_name_query()

        raise ValueError("Invalid Query Type")

    def _run_name_query(self):
        """ Runs a name query - runs if self.type === NAME_TYPE """
        raise NotImplementedError()

    def _run_location_query(self) -> List[Tribe]:
        """ Runs a location query - runs if self.type === LOCATION_TYPE """

        min_lat, max_lat, min_long, max_long = self._calculate_bounds()

        results = Tribe.query \
            .filter(Tribe.latitude >= min_lat) \
            .filter(Tribe.latitude <= max_lat) \
            .filter(Tribe.longitude >= min_long) \
            .filter(Tribe.longitude <= max_long).all()

        return sorted(results, key=self._sort_by_distance)

    def _sort_by_distance(self, tribe: Tribe):
        """ Returns the rough distance a tribe is from the search location """
        lat_diff = abs(tribe.latitude - self.latitude) * \
            DistanceConversions.LAT_TO_KM

        long_diff = abs(tribe.longitude - self.longitude) * \
            radians(tribe.latitude) * DistanceConversions.LONG_TO_KM

        return sqrt(lat_diff ** 2 + long_diff ** 2)

    def _calculate_bounds(self):
        """
        This is a fairly crude function for getting a rough search area from
        coordinates and a metre radius - it's not perfect but it's good enough

        ASSUMPTIONS:
        Latitude: 1 deg = 110.574km
        Longitude: 1 deg = 111.320*cos(latitude)km
        """

        lat_rad = radians(self.latitude)

        lat_range = (self.radius / 1000) / DistanceConversions.LAT_TO_KM
        min_lat = self.latitude - lat_range
        max_lat = self.latitude + lat_range

        long_range = ((self.radius / 1000)) / \
            (DistanceConversions.LONG_TO_KM * cos(lat_rad))

        min_long = self.longitude - long_range
        max_long = self.longitude + long_range

        return min_lat, max_lat, min_long, max_long

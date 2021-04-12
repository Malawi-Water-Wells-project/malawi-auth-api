from app.main.models.tribe import Tribe
from datetime import datetime
from .. import db
from typing import List, Union
from uuid import uuid4
import redis
import json
from math import dist, radians, cos, sqrt
from app.main.constants import DistanceConversions

r = redis.Redis(host="localhost", port=6379, db=0)


def save_new_tribe(data):
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
    return Tribe.query.filter_by(public_id=tribe_id).first()


def get_tribe_by_id(tribe_id) -> Union[Tribe, None]:
    return Tribe.query.filter_by(id=tribe_id).first()


def create_tribe_join_token(tribe_id, tribe_name):
    token = str(uuid4())

    token_data = {
        "token": token,
        "tribe_id": tribe_id,
        "tribe_name": tribe_name
    }

    ok = r.setex(f"jointoken:{token}", 15 * 60, json.dumps(token_data))

    if ok:
        return token_data

    raise Exception("Failed to set jointoken")


def check_join_token(token):
    if "token" in token:
        data = r.get(f"jointoken:{token.get('token')}")
        print(data)
        return True

    raise Exception("Oops!")


def lookup_join_token(token):
    response = r.get(f"jointoken:{token}")

    if response is None:
        return None

    return json.loads(response)


class TribeSearchQuery:
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

    def run_query(self):
        if self.type == self.LOCATION_TYPE:
            return self._run_location_query()
        elif self.type == self.NAME_TYPE:
            return self._run_name_query()

    def _run_name_query(self):
        raise NotImplementedError()

    def _run_location_query(self):
        min_lat, max_lat, min_long, max_long = self._calculate_bounds()

        results = Tribe.query \
            .filter(Tribe.latitude >= min_lat) \
            .filter(Tribe.latitude <= max_lat) \
            .filter(Tribe.longitude >= min_long) \
            .filter(Tribe.longitude <= max_long).all()

        return self._rank_by_distance(results)

    def _rank_by_distance(self, results: List[Tribe]):
        def sort_by_distance(x):
            lat_diff = abs(x.latitude - self.latitude) * \
                DistanceConversions.LAT_TO_KM

            long_diff = abs(x.longitude - self.longitude) * \
                radians(x.latitude) * DistanceConversions.LONG_TO_KM

            return sqrt(lat_diff ** 2 + long_diff ** 2)

        return sorted(results, key=sort_by_distance)

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

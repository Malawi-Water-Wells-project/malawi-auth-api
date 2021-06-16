"""
Created 05/02/2021
DB Access Service for Tribes
"""

# import json
# from math import cos, radians, sqrt
from app.main.models.tribe import Tribe
from typing import Union
# from uuid import uuid4
# from app.main.constants import DistanceConversions
# from app.main.models.tribe import Tribe


# from app.main.service.abstract_service import AbstractRedisService

class TribeService:
    @classmethod
    def get_by_id(cls, tribe_id: str) -> Union[Tribe, None]:
        """ Retrieves a tribe by it's ID """
        try:
            return Tribe.get(tribe_id)
        except Tribe.DoesNotExist:
            return None

# class TribeService(AbstractRedisService):
#     #pylint: disable=no-member
#     MODEL = Tribe

#     @classmethod
#     def get_by_public_id(cls, public_id) -> Union[Tribe, None]:
#         return cls.filter(public_id=public_id).first()

#     @classmethod
#     def generate_join_token(cls, tribe: Tribe):
#         """ Creates a token that can be used to join a Tribe """
#         token = str(uuid4())
#         token_data = {
#             "token": token,
#             "tribe_id": tribe.public_id,
#             "tribe_name": tribe.name
#         }

#         success = cls.redisClient().setex(
#             f"jointoken:{token}", 15 * 60, json.dumps(token_data))

#         print(success)

#         if success:
#             return token_data

#         raise Exception("Failed to set jointoken")

#     @classmethod
#     def check_join_token(cls, token: dict):
#         """ Validates a Join Token """

#         if "token" in token:
#             data = cls.redisClient().get(
#                 f"jointoken:{token.get('token', None)}")
#             return True

#         raise Exception("Oops!")

#     @classmethod
#     def lookup_join_token(cls, token: str) -> dict:
#         """ Queries Redis for a Join Token """
#         response = cls.redisClient().get(f"jointoken:{token}")
#         if response is None:
#             return None
#         return json.loads(response)


# class TribeSearchQuery:
#     """
#     Handler for Tribe Searches
#     Implements a fuzzy-match name search (TODO) and a location-based search
#     """
#     LOCATION_TYPE = "location"
#     NAME_TYPE = "name"

#     def __init__(
#         self,
#         search_type: str = None,
#         latitude: float = None,
#         longitude: float = None,
#         radius: int = None,
#         name: str = None
#     ):
#         self.type = search_type
#         self.latitude = latitude
#         self.longitude = longitude
#         self.radius = radius
#         self.name = name

#     def run_query(self) -> List[Tribe]:
#         """ Runs the configured query """
#         if self.type == self.LOCATION_TYPE:
#             return self._run_location_query()
#         if self.type == self.NAME_TYPE:
#             return self._run_name_query()

#         raise ValueError("Invalid Query Type")

#     def _run_name_query(self):
#         """ Runs a name query - runs if self.type === NAME_TYPE """
#         raise NotImplementedError()

#     def _run_location_query(self) -> List[Tribe]:
#         """ Runs a location query - runs if self.type === LOCATION_TYPE """

#         min_lat, max_lat, min_long, max_long = self._calculate_bounds()

#         results = Tribe.query \
#             .filter(Tribe.latitude >= min_lat) \
#             .filter(Tribe.latitude <= max_lat) \
#             .filter(Tribe.longitude >= min_long) \
#             .filter(Tribe.longitude <= max_long).all()

#         return sorted(results, key=self._sort_by_distance)

#     def _sort_by_distance(self, tribe: Tribe):
#         """ Returns the rough distance a tribe is from the search location """
#         lat_diff = abs(tribe.latitude - self.latitude) * \
#             DistanceConversions.LAT_TO_KM

#         long_diff = abs(tribe.longitude - self.longitude) * \
#             radians(tribe.latitude) * DistanceConversions.LONG_TO_KM

#         return sqrt(lat_diff ** 2 + long_diff ** 2)

#     def _calculate_bounds(self):
#         """
#         This is a fairly crude function for getting a rough search area from
#         coordinates and a metre radius - it's not perfect but it's good enough

#         ASSUMPTIONS:
#         Latitude: 1 deg = 110.574km
#         Longitude: 1 deg = 111.320*cos(latitude)km
#         """

#         lat_rad = radians(self.latitude)

#         lat_range = (self.radius / 1000) / DistanceConversions.LAT_TO_KM
#         min_lat = self.latitude - lat_range
#         max_lat = self.latitude + lat_range

#         long_range = ((self.radius / 1000)) / \
#             (DistanceConversions.LONG_TO_KM * cos(lat_rad))

#         min_long = self.longitude - long_range
#         max_long = self.longitude + long_range

#         return min_lat, max_lat, min_long, max_long

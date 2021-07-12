"""
Created 05/02/2021
Application Constants
"""
#pylint: disable=too-few-public-methods


class UserRoles:
    """ Roles that can be associated with Users """
    ADMIN = "admin"
    VILLAGE_ADMIN = "villageadmin"
    USER = "user"


class DistanceConversions:
    """ Lat/Long Degrees to Kilometer conversions """
    LAT_TO_KM = 110.574
    LONG_TO_KM = 111.320


class ResponseStatus:
    """ Response Statuses """
    SUCCESS = "Success"
    FAILURE = "Failure"
    MIXED = "Mixed"

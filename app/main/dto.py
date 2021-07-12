"""
Created 05/02/2021
API Data Transfer Objects
"""
from flask_restx import Namespace, fields


class RootDto:
    """ Data Transfer Object for root-level controllers """
    api = Namespace("root", description="Top-Level API Operations")


class TribeDto:
    """ Data Transfer Object for the Tribes Controller """
    api = Namespace("tribe", description="Tribe Operations")
    tribe = api.model("tribe", {
        "name": fields.String(required=True, description="Tribe Name"),
        "latitude": fields.Float(required=True, description="Latitude of Tribe"),
        "longitude": fields.Float(required=True, description="Longitude of Tribe")
    })
    admin = api.model("admin", {
        "name": fields.String(required=True, description="Admin Name"),
        "username": fields.String(required=True, description="Admin Username"),
        "password": fields.String(required=True, description="Admin Password")
    })
    new_user = api.model("newuser", {
        "token": fields.String(required=True, description="Join Token"),
        "username": fields.String(required=True, description="Username"),
        "password": fields.String(required=True, description="Password"),
        "name": fields.String(required=True, description="Name")
    })


class AuthDto:
    """ Data Transfer Object for the Auth Controller """
    api = Namespace("auth", description="Authentication Operations")
    credentials = api.model("credentials", {
        "username": fields.String(required=True, description="Username"),
        "password": fields.String(required=True, description="Password")
    })


class WellDto:
    """ Data Transfer Object for the Wells Controller """
    api = Namespace("well", description="Well Operations")


class UserDto:
    """ Data Transfer Object for the Users Controller """
    api = Namespace("user", description="User Operations")

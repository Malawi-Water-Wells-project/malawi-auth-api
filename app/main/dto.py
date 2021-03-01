from flask_restx import Namespace, fields


class TribeDto:
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
    api = Namespace("auth", description="Authentication Operations")
    credentials = api.model("credentials", {
        "username": fields.String(required=True, description="Username"),
        "password": fields.String(required=True, description="Password")
    })


class WellDto:
    api = Namespace("well", description="Well Operations")

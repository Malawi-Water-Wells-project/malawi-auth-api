from app.main.constants import UserRoles
from app.main.service.tribe_service import get_tribe_by_public_id
from app.main.util.jwt import validate_access_token
from flask.globals import request
from functools import wraps


def user_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if token is None:
            return {
                "status": "Failure",
                "message": "Not Authorized"
            }, 401

        error, payload = validate_access_token(token)
        if error is not None:
            return {
                "status": "Failure",
                "message": error
            }, 401

        return f(*args, **kwargs, jwt=payload)

    return wrapper


def user_is_tribe_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        tribe_id = kwargs.get("tribe_id")
        jwt = kwargs.get("jwt")
        tribe = get_tribe_by_public_id(tribe_id)

        if tribe is None:
            return {
                "status": "Failure",
                "message": "Tribe not found"
            }, 404

        if jwt.get("role") != UserRoles.TRIBE_ADMIN or jwt.get("tribe_id") != tribe.id:
            return {
                "status": "Failure",
                "message": "You are not authorized to perform this action"
            }, 403

        return f(*args, **kwargs)

    return wrapper

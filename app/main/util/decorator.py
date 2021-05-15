"""
Created 08/02/2021
Decorators for wrapping requests
"""
from functools import wraps

from app.main.constants import UserRoles
from app.main.service.tribe_service import get_tribe_by_public_id
from app.main.util.jwt import validate_access_token
from flask.globals import request


def user_logged_in(wrapped_func):
    """ Decorator to ensure the request comes from a logged in user """
    @wraps(wrapped_func)
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

        return wrapped_func(*args, **kwargs, jwt=payload)

    return wrapper


def user_is_tribe_admin(wrapped_func):
    """ Decorator to ensure that the incoming request comes from a Tribe Admin of their Tribe """
    @wraps(wrapped_func)
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

        return wrapped_func(*args, **kwargs, tribe=tribe)

    return wrapper

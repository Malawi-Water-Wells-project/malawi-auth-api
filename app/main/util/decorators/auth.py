"""
Created 20/05/2021
Authentication Decorators
"""
from functools import wraps

from app.main.constants import UserRoles
from app.main.controllers.resource import Resource
from app.main.service.tribe_service import get_tribe_by_public_id
from app.main.service.user_service import find_user_by_public_id
from app.main.util.jwt import validate_access_token
from app.main.util.logger import AppLogger
from flask.globals import request


class AuthDecorators:
    """ Decorators for various auth control flows """
    logger = AppLogger()

    @classmethod
    def ensure_logged_in(cls, wrapped_func):
        """
        Ensures that the incoming request is valid and authorised
        Pass user info to following requests
        """
        @wraps(wrapped_func)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if token is None:
                cls.logger.log("AUTH001")
                return Resource.format_failure(401, "Not Authorized")

            error, payload = validate_access_token(token)

            if error is not None:
                cls.logger.log("AUTH002")
                return Resource.format_failure(401, error)

            cls.logger.log("AUTH003")
            return wrapped_func(*args, **kwargs, jwt=payload)

        return wrapper

    @staticmethod
    def _get_role_for_user(kwargs: dict):
        jwt = kwargs.get("jwt")
        print(jwt)

    @classmethod
    def ensure_is_admin(cls, wrapped_func):
        """
        Ensures that the incoming request is from an administrator
        Prerequisites: AuthDecorators.ensure_logged_in
        """

        @wraps(wrapped_func)
        @cls.ensure_logged_in
        def wrapper(*args, **kwargs):
            return wrapped_func(*args, **kwargs)

        return wrapper

    @classmethod
    def ensure_is_tribe_admin(cls, wrapped_func):
        """
        Ensures that the incoming request is from a tribe admin
        Prerequisites: Authdecorators.ensure_logged_in
        """
        @wraps(wrapped_func)
        @cls.ensure_logged_in
        def wrapper(*args, **kwargs):
            tribe_id = kwargs.get("tribe_id")
            jwt = kwargs.get("jwt")

            tribe = get_tribe_by_public_id(tribe_id)

            if tribe is None:
                return Resource.format_failure(404, "Tribe not found")

            role = jwt.get("role")
            token_tribe_id = jwt.get("tribe_id")

            if role and role == UserRoles.TRIBE_ADMIN and token_tribe_id == tribe.id:
                return wrapped_func(*args, **kwargs, tribe=tribe)
            return Resource.format_failure(403, "You are not authorized to perform this action.")

        return wrapper

    @classmethod
    def ensure_user_access(cls, wrapped_func):
        """
        Ensures that the request is authorized to view/edit this user
        Prerequisites: AuthDecorators.ensure_logged_in
        """
        @wraps(wrapped_func)
        @cls.ensure_logged_in
        def wrapper(*args, **kwargs):
            user_id = kwargs.get("user_id")
            user = find_user_by_public_id(user_id)
            jwt = kwargs.get("jwt")

            if user is None:
                return Resource.format_failure(404, "User not found")

            # Admin has superuser rights
            if user.role == UserRoles.ADMIN:
                return wrapped_func(*args, **kwargs, user=user)

            # TribeAdmin has superuser rights over their tribe
            # TODO: Tribeadmin edit logic

            if jwt.get("user_id") != user.id:
                return Resource.format_failure(401, "You are not authorized to perform this action")

            return wrapped_func(*args, **kwargs, user=user)

        return wrapper

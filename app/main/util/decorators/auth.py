"""
Created 20/05/2021
Authentication Decorators
"""
from app.main.service.village_service import VillageService
from functools import wraps

from app.main.constants import UserRoles
from app.main.controllers.resource import Resource
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

    @classmethod
    def ensure_is_admin(cls, wrapped_func):
        """
        Ensures that the incoming request is from an administrator
        Prerequisites: AuthDecorators.ensure_logged_in
        """

        @wraps(wrapped_func)
        @cls.ensure_logged_in
        def wrapper(*args, **kwargs):
            role = kwargs["jwt"]["role"]
            if role != UserRoles.ADMIN:
                return Resource.format_failure(403, "You are not authorized to perform this action.")

            return wrapped_func(*args, **kwargs)

        return wrapper

    @classmethod
    def ensure_is_village_admin(cls, wrapped_func):
        """
        Ensures that the incoming request is from a village admin
        Prerequisites: AuthDecorators.ensure_logged_in
        """
        @wraps(wrapped_func)
        @cls.ensure_logged_in
        def wrapper(*args, **kwargs):
            village = VillageService.get_by_id(kwargs["village_id"])
            if village is None:
                return Resource.format_failure(404, "Village not found")

            role = kwargs["jwt"]["role"]
            if role == UserRoles.ADMIN:
                return wrapped_func(*args, **kwargs, village=village)

            if role != UserRoles.VILLAGE_ADMIN:
                return Resource.no_permissions_for_action()

            user_village_id = kwargs["jwt"].get("village_id")
            if user_village_id is None:
                return Resource.no_permissions_for_action()

            if user_village_id != village.village_id:
                return Resource.no_permissions_for_action()

            return wrapped_func(*args, **kwargs, village=village)

        return wrapper

    # @classmethod
    # def ensure_user_access(cls, wrapped_func):
    #     """
    #     Ensures that the request is authorized to view/edit this user
    #     Prerequisites: AuthDecorators.ensure_logged_in
    #     """
    #     @wraps(wrapped_func)
    #     @cls.ensure_logged_in
    #     def wrapper(*args, **kwargs):
    #         user_id = kwargs.get("user_id")
    #         user = UserService.get_by_public_id(user_id)
    #         jwt = kwargs.get("jwt")

    #         if user is None:
    #             return Resource.format_failure(404, "User not found")

    #         # Admin has superuser rights
    #         if user.role == UserRoles.ADMIN:
    #             return wrapped_func(*args, **kwargs, user=user)

    #         # TribeAdmin has superuser rights over their tribe
    #         # TODO: Tribeadmin edit logic

    #         if jwt.get("user_id") != user.id:
    #             return Resource.format_failure(401, "You are not authorized to perform this action")

    #         return wrapped_func(*args, **kwargs, user=user)

    #     return wrapper

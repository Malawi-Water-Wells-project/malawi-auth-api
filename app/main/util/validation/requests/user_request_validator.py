"""
Created: 20/05/2021
User Request Validator
"""
from app.main.service.tribe_service import (get_tribe_by_public_id,
                                            lookup_join_token)
from app.main.service.user_service import find_user_by_username
from app.main.util.validation.rules import CommonRules
from flask.globals import request

from .abstract_request_validator import AbstractRequestValidator


class CreateUserValidator(AbstractRequestValidator):
    """ Create User Validator """
    SCHEMA = {
        "name":  CommonRules.NAME.required,
        "username": CommonRules.USERNAME.required,
        "password": CommonRules.PASSWORD.required,
        "tribe_id": CommonRules.TRIBE_ID
    }

    def postvalidation(self):
        """
        Ensure that the username is unique and the tribe exists if provided
        """
        existing_user = find_user_by_username(request.json.get("username"))

        if existing_user is not None:
            self.add_error("username", "Username already exists")
            return

        tribe_id = request.json.get("tribe_id")
        if tribe_id is None:
            return

        tribe = get_tribe_by_public_id(tribe_id)
        if tribe is None:
            self.add_error("tribe_id", "Tribe not found")


class PatchUserValidator(AbstractRequestValidator):
    """ Validator for updating a user """
    SCHEMA = {
        "name": CommonRules.NAME,
        "username": CommonRules.USERNAME,
        "role": CommonRules.ROLE,
        "tribe_id": CommonRules.TRIBE_ID
    }


class ClaimTokenValidator(AbstractRequestValidator):
    """ Validator for POST /users/claim-token """
    SCHEMA = {
        "name": CommonRules.NAME.required,
        "username": CommonRules.USERNAME.required,
        "password": CommonRules.PASSWORD.required,
        "token": CommonRules.TOKEN.required
    }

    def postvalidation(self):
        """ Check that the token is valid and the tribe exists """
        token = lookup_join_token(request.json.get("token"))

        if token is None:
            self.add_error("token", "Token does not exist")
            return

        tribe_id = token.get("tribe_id")
        if not tribe_id:
            self.add_error("token", "Invalid Token")

        tribe = get_tribe_by_public_id(tribe_id)
        if tribe is None:
            self.add_error("token", "Invalid Token")

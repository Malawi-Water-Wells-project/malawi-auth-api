"""
Created: 20/05/2021
User Request Validator
"""

from app.main.service.village_service import VillageService
from app.main.service.user_service import UserService
from app.main.util.validation.rules import CommonRules
from flask.globals import request

from .abstract_request_validator import AbstractRequestValidator


class CreateUserValidator(AbstractRequestValidator):
    """ Create User Validator """
    SCHEMA = {
        "name":  CommonRules.NAME.required,
        "username": CommonRules.USERNAME.required,
        "password": CommonRules.PASSWORD.required,
        "village_id": CommonRules.VILLAGE_ID,
        "role": CommonRules.ROLE,
    }

    def postvalidation(self):
        """
        Ensure that the username is unique and the village exists if provided
        """
        existing_user = UserService.get_by_username(
            request.json.get("username"))

        if existing_user is not None:
            self.add_error("username", "Username already exists")
            return

        village_id = request.json.get("village_id")
        if village_id is None:
            self.lookup_cache.add("village", None)
            return

        village = VillageService.get_by_id(village_id)
        if village is None:
            self.add_error("village_id", "Village not found")
        self.lookup_cache.add("village", village)


class PatchUserValidator(AbstractRequestValidator):
    """ Validator for updating a user """
    SCHEMA = {
        "name": CommonRules.NAME,
        "username": CommonRules.USERNAME,
        "role": CommonRules.ROLE,
        "village_id": CommonRules.VILLAGE_ID
    }


class ClaimTokenValidator(AbstractRequestValidator):
    """ Validator for POST /users/claim-token """
    SCHEMA = {
        "name": CommonRules.NAME.required,
        "username": CommonRules.USERNAME.required,
        "password": CommonRules.PASSWORD.required,
        "token": CommonRules.STRING.required
    }

    def postvalidation(self):
        """ Check that the token is valid and the village exists """
        token = VillageService.lookup_join_token(request.json.get("token"))

        if token is None:
            self.add_error("token", "Token does not exist")
            return

        village_id = token.get("village_id")
        if not village_id:
            self.add_error("token", "Invalid Token")

        village = VillageService.get_by_id(village_id)

        if village is None:
            self.add_error("token", "Invalid Token")

        self.lookup_cache["village"] = village

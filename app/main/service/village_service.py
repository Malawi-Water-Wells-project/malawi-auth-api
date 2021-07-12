"""
Created 05/02/2021
DB Access Service for Villages
"""

from app.main.constants import UserRoles
from app.main.models.user import User
from datetime import datetime
from app.main.models.join_token import JoinToken
from app.main.models.village import Village
from typing import List, Union


class VillageService:
    """ Village DB Access Service """

    @classmethod
    def get_by_id(cls, village_id: str) -> Union[Village, None]:
        """ Retrieves a village by it's ID """
        try:
            return Village.get(village_id)
        except Village.DoesNotExist:
            return None

    @classmethod
    def create_join_token(cls, village: Village) -> JoinToken:
        """
        Returns a Join Token for the village.
        If a join token already exists, renew the TTL
        """
        token = JoinToken(village_id=village.village_id,
                          village_name=village.name)
        token.save()
        return token

    @classmethod
    def lookup_join_token(cls, token_id: str) -> Union[JoinToken, None]:
        """ Retrieves a Join Token from the DB """
        try:
            token = JoinToken.get(token_id)
            if token.ttl < datetime.now():
                return token
            return None
        except JoinToken.DoesNotExist:
            return None

    @classmethod
    def get_villageadmins(cls, village: Village) -> List[User]:
        """ Returns all admins for a Village """
        return [
            user for user
            in User.batch_get(village.users)
            if user.role == UserRoles.VILLAGE_ADMIN
        ]

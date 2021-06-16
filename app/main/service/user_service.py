"""
Created 05/02/2021
DB Access Service for Users
"""
# from app.main.service.abstract_service import AbstractService
# from datetime import datetime
from typing import Union
# from uuid import uuid4

# from app.main.constants import UserRoles
# from app.main.models.user import User, db


# class UserService(AbstractService):
#     MODEL = User

#     @classmethod
#     def get_by_user_id(cls, user_id: str):
#         return cls.filter(user_id=user_id).first()

#     @classmethod
#     def get_by_username(cls, username: str) -> Union[User, None]:
#         return cls.filter(username=username).first()

#     @classmethod
#     def get_by_public_id(cls, public_id: str) -> Union[User, None]:
#         return cls.filter(public_id=public_id).first()

from app.main.models.user import User


class UserService():
    """ DynamoDB User Service """

    @classmethod
    def get_by_username(cls, username: str) -> Union[User, None]:
        """ Gets a user by their username """
        try:
            return User.get(username)
        except User.DoesNotExist:
            return None

    @classmethod
    def get_by_id(cls, user_id: str) -> Union[User, None]:
        """ Gets a user by their user_id """
        try:
            return next(User.index.query(user_id))
        except StopIteration:
            return None

"""
Created 05/02/2021
DB Access Service for Users
"""
from typing import Union
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

"""
Created 05/02/2021
DB Access Service for Users
"""
from app.main.service.abstract_service import AbstractService
from datetime import datetime
from typing import List, Union
from uuid import uuid4

from app.main.constants import UserRoles
from app.main.models.user import User, db


class UserService(AbstractService):
    MODEL = User

    @classmethod
    def get_by_user_id(cls, user_id: str):
        return cls.filter(user_id=user_id).first()

    @classmethod
    def get_by_username(cls, username: str) -> Union[User, None]:
        return cls.filter(username=username).first()

    @classmethod
    def get_by_public_id(cls, public_id: str) -> Union[User, None]:
        return cls.filter(public_id=public_id).first()

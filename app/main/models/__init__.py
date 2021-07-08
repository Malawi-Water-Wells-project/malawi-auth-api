"""
Created 05/02/2021
Ensures the tables for models and provides exports
"""
from .user import User
from .tribe import Tribe
from .refresh_token import RefreshToken
from typing import Set
from pynamodb.models import Model

ALL_MODELS: Set[Model] = {User, Tribe, RefreshToken}


def ensure_tables():
    """ Ensures that all the tables have been created in DynamoDB """

    for model in ALL_MODELS:
        if not model.exists():
            model.create_table()

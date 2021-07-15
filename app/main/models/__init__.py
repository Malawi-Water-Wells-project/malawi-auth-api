"""
Created 05/02/2021
Empty __init__.py for models
"""

from typing import Set
from pynamodb.models import Model
from app.main.models.well import Well
from app.main.models.village import Village
from app.main.models.user import User
from app.main.models.refresh_token import RefreshToken
from app.main.models.join_token import JoinToken


ALL_TABLES: Set[Model] = {JoinToken, RefreshToken, User, Village, Well}


def setup_test_tables(env_name: bool):
    """ Setup Test Tables """
    if env_name != "LOCAL":
        return

    for table in ALL_TABLES:
        if not table.exists():
            table.create_table()

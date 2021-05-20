"""
Created 05/02/2021
DB Access Service for Users
"""
from datetime import datetime
from typing import List, Union
from uuid import uuid4

from app.main.constants import UserRoles
from app.main.models.user import User, db


def create_new_user(data: dict, tribe_id: str, role: str) -> User:
    """
    Creates a new user in the DB. Expected data: "name", "username", "password"
    """
    new_user = User(
        tribe_id=tribe_id,
        public_id=str(uuid4()),
        name=data.get("name"),
        username=data.get("username"),
        role=role,
        created_on=datetime.utcnow()
    )

    new_user.password = data.get("password")

    db.session.add(new_user)
    db.session.commit()

    return new_user


def update_user(user: User) -> None:
    """ Updates a User in the DB """
    db.session.add(user)
    db.session.commit()


def find_user_by_id(user_id) -> Union[User, None]:
    """ Queries the DB for a user by ID """
    return User.query.filter_by(id=user_id).first()


def find_user_by_public_id(public_id) -> Union[User, None]:
    """ Queries the DB for a user by Public ID """
    return User.query.filter_by(public_id=public_id).first()


def find_user_by_username(username) -> Union[User, None]:
    """ Queries the DB for a user by username """
    return User.query.filter_by(username=username).first()

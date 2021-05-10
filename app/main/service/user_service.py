from typing import Union
from app.main.models.user import User
from app.main.constants import UserRoles
from uuid import uuid4
from datetime import datetime
from .. import db


def create_new_user(data, tribe_id, role):
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


def update_user(user):
    db.session.add(user)
    db.session.commit()


def find_user_by_id(id) -> Union[User, None]:
    return User.query.filter_by(id=id).first()


def find_user_by_username(username) -> Union[User, None]:
    return User.query.filter_by(username=username).first()


def get_admins_by_tribe(tribe_id):
    return User.query.filter_by(tribe_id=tribe_id, role=UserRoles.TRIBE_ADMIN).all()

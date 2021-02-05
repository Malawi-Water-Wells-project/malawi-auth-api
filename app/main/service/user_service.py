from typing import Union
from app.main.models.user import User
from uuid import uuid4
from datetime import datetime
from .. import db


def create_new_user(data, tribe_id, role):
    new_user = User(
        tribe_id=tribe_id,
        public_id=str(uuid4()),
        name=data.get("name"),
        role=role,
        created_on=datetime.utcnow()
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user


def update_user(user):
    db.session.add(user)
    db.session.commit()


def find_user_by_username(username) -> Union[User, None]:
    return User.query.filter_by(username=username).first()

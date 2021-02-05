from app.main.models.tribe import Tribe
from datetime import datetime
from .. import db
from typing import Union
from uuid import uuid4


def save_new_tribe(data):
    new_tribe = Tribe(
        public_id=str(uuid4()),
        name=data.get("name"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        created_on=datetime.utcnow()
    )
    db.session.add(new_tribe)
    db.session.commit()

    return new_tribe


def get_tribe_by_public_id(tribe_id) -> Union[Tribe, None]:
    return Tribe.query.filter_by(public_id=tribe_id).first()

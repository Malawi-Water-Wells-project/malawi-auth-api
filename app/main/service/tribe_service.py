from app.main.models.tribe import Tribe
from datetime import datetime
from .. import db
from typing import Union
from uuid import uuid4
import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0)


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


def get_tribe_by_id(tribe_id) -> Union[Tribe, None]:
    return Tribe.query.filter_by(id=tribe_id).first()


def create_tribe_join_token(tribe_id, tribe_name):
    token = str(uuid4())

    token_data = {
        "token": token,
        "tribe_id": tribe_id,
        "tribe_name": tribe_name
    }

    ok = r.setex(f"jointoken:{token}", 15 * 60, json.dumps(token_data))

    if ok:
        return token_data

    raise Exception("Failed to set jointoken")


def check_join_token(token):
    if "token" in token:
        data = r.get(f"jointoken:{token.get('token')}")
        print(data)
        return True

    raise Exception("Oops!")


def lookup_join_token(token):
    response = r.get(f"jointoken:{token}")

    if response is None:
        return None

    return json.loads(response)

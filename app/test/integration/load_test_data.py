"""
Created 16/06/2021
Integration Test Data Setup
"""

from app.main.models.tribe import Tribe
from ...main.models.user import User
import os
import json

BASE_DATA_PATH = "app/test/integration/data/"


def data_generator(file_name: str):
    full_path = os.path.abspath(f"{BASE_DATA_PATH}{file_name}")
    with open(full_path) as input_file:
        for line in input_file.readlines():
            if not line:
                continue
            yield json.loads(line.strip())


def load_users():
    """ Load Users into the DB """
    print("=== Loading Users ===")
    if not User.exists():
        User.create_table()

    for record in data_generator("users.jsonl"):
        try:
            user = User.get(record["username"])
        except User.DoesNotExist:
            user = User(**record)
            user.set_password(record["password"])
            user.save()
        print(f"Loaded User: Username='{user.username} ID='{user.user_id}'")


def load_tribes():
    """ Load Tribes into the DB """
    print("=== Loading Tribes ===")
    if not Tribe.exists():
        Tribe.create_table()

    for record in data_generator("tribes.jsonl"):
        try:
            tribe = Tribe.get(record["tribe_id"])
        except Tribe.DoesNotExist:
            tribe = Tribe(**record)
            tribe.save()
        print(f"Loaded Tribe: Name='{tribe.name}' ID='{tribe.tribe_id}'")


def main():
    """ Main Script Entrypoint """
    print("""=== Integration Test Data Load ===""")
    load_users()
    load_tribes()


if __name__ == "__main__":
    main()

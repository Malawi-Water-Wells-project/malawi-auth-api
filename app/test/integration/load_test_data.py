"""
Created 16/06/2021
Integration Test Data Setup
"""

from app.main.models.village import Village
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

    for record in data_generator("users.jsonl"):
        try:
            user = User.get(record["username"])
        except User.DoesNotExist:
            user = User(**record)
            user.set_password(record["password"])
            user.save()
        print(f"Loaded User: Username='{user.username} ID='{user.user_id}'")


def load_villages():
    """ Load Villages into the DB """
    print("=== Loading Villages ===")

    for record in data_generator("villages.jsonl"):
        try:
            village = Village.get(record["village_id"])
        except Village.DoesNotExist:
            village = Village(**record)
            village.save()
        print(
            f"Loaded Village: Name='{village.name}' ID='{village.village_id}'")


def main():
    """ Main Script Entrypoint """
    print("""=== Integration Test Data Load ===""")
    load_users()
    load_villages()


if __name__ == "__main__":
    main()

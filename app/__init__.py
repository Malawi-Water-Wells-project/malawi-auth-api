"""
Created 05/03/2021
__init__.py for setting up the application and the DB tables
"""
import os

from app.main import Application
from app.main.models import db


def setup_test_environment():
    app = Application(os.environ.get("ENV", "dev"))

    with app.flask.app_context():
        # db.drop_all()
        db.create_all()


setup_test_environment()

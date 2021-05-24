"""
Created 05/03/2021
__init__.py for setting up the application and the DB tables
"""
from app.main.models import db
from app.main import Application
import os
from dotenv import load_dotenv

load_dotenv()


def setup_test_environment():
    app = Application(os.environ.get("ENV", "prod"))

    with app.flask.app_context():
        # db.drop_all()
        db.create_all()


setup_test_environment()

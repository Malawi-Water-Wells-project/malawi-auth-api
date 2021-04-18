from app.main import Application
from app.main.models import db
import os

def setup_test_environment():
    app = Application(os.environ.get("ENV", "prod"))

    with app.flask.app_context():
        db.drop_all()
        db.create_all()


setup_test_environment()

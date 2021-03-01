from app.main import Application
from app.main.models import db


def setup_test_environment():
    app = Application("test")

    with app.flask.app_context():
        db.drop_all()
        db.create_all()


setup_test_environment()

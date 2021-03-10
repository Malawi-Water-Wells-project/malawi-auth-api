from app.main import Application
from flask_script import Command, Option


app = Application("prod")
flask = app.flask


if __name__ == "__main__":
    flask.run()

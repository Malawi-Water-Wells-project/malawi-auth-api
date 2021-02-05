import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.main import Application
from app.main.models.db import db

app = Application(os.getenv("BOILERPLATE_ENV") or "dev")

app.flask.app_context().push()

manager = Manager(app.flask)
migrate = Migrate(app.flask, db)


manager.add_command("db", MigrateCommand)


@manager.command
def run():
    app.flask.run()


@manager.command
def test():
    """ Runs the unit tests """
    tests = unittest.TestLoader().discover("app/test", pattern="*_test.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()

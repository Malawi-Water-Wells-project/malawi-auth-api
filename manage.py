"""
Created 05/02/2021
Management Script
"""

import csv
import os
import unittest
from datetime import datetime
from uuid import uuid4

import inquirer
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main import Application
from app.main.models import db

app = Application(os.getenv("ENV") or "dev")

app.flask.app_context().push()

manager = Manager(app.flask)
migrate = Migrate(app.flask, db)


manager.add_command("db", MigrateCommand)


@manager.command
def run():
    """ Run the application in dev mode """
    app.flask.run(host="0.0.0.0", port=8080, debug=True)


@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', type=int, default=8080)
@manager.option('-w', '--workers', dest='workers', type=int, default=4)
def run_prod(host, port, workers):
    """ Run the application in production mode """
    from gunicorn.app.base import Application as GunicornApplication

    migrate.init_app(app, db)

    class FlaskApplication(GunicornApplication):
        def init(self, parser, opts, args):
            return {
                "bind": f"{host}:{port}",
                "workers": workers
            }

        def load(self):
            return app.flask

    gunicorn_app = FlaskApplication()
    return gunicorn_app.run()


@manager.option("-i", "--input", dest="input_location", help="CSV File Input")
def load_wells(input_location):
    """ Load Well data from a CSV """
    file_location = os.path.join(os.getcwd(), input_location)
    with open(file_location) as input_file:

        for row in csv.reader(input_file):
            well_id, country, district, sub_district, village, latitude, _, longitude = row
            db.session.add(Well(
                well_id=well_id,
                country=country,
                district=district,
                sub_district=sub_district,
                village=village,
                latitude=float(latitude),
                longitude=float(longitude)
            ))

        db.session.commit()


@manager.command
def create_user():
    """ Management Script for creating users """
    print("=== Create User ===")
    questions = [
        inquirer.Text("name", message="Full Name"),
        inquirer.Text("username", message="Username"),
        inquirer.Password("password", message="Password"),
        inquirer.Password("password_repeat", message="Confirm Password"),
        inquirer.Text("tribe_id", message="Tribe ID (optional)"),
        inquirer.List("role", message="Role", choices=[
                      UserRoles.USER, UserRoles.ADMIN, UserRoles.TRIBE_ADMIN])
    ]

    answers = inquirer.prompt(questions)
    name = answers.get("name")
    username = answers.get("username")
    password = answers.get("password")
    password_repeat = answers.get("password_repeat")
    tribe_id = answers.get("tribe_id")
    role = answers.get("role")

    if not tribe_id:
        tribe_id = None

    if password_repeat != password:
        print("Passwords do not match!")
        return

    user = User(
        tribe_id=tribe_id,
        public_id=str(uuid4()),
        username=username,
        name=name,
        role=role,
        created_on=datetime.utcnow()
    )
    user.password = password

    print("Do you want to add this user to the database?")
    print(user)

    answers = inquirer.prompt([inquirer.Confirm("confirm", message="Confirm")])

    confirm = answers.get("confirm")
    if not confirm:
        return

    db.session.add(user)
    db.session.commit()

    print(f"Successfully added user: {user}")


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

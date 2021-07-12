"""
Created 05/02/2021
Management Script
"""

import os
import unittest
import inquirer

from flask_script import Manager
from app.main import Application
from app.main.constants import UserRoles
from app.main.models.user import User

app = Application(os.getenv("ENV") or "dev")
manager = Manager(app.flask)


@manager.command
def run():
    """ Run the application in dev mode """
    app.flask.run(host="0.0.0.0", port=8080, debug=True,
                  load_dotenv=True, use_evalex=False)


@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', type=int, default=8080)
@manager.option('-w', '--workers', dest='workers', type=int, default=4)
def run_prod(host, port, workers):
    """ Run the application in production mode """
    # pylint: disable=import-outside-toplevel
    from gunicorn.app.base import Application as GunicornApplication

    class FlaskApplication(GunicornApplication):
        """ Gunicorn FlaskApplication Wrapper """

        def init(self, _parser, _opts, _args):
            return {
                "bind": f"{host}:{port}",
                "workers": workers
            }

        def load(self):
            return app.flask

    return FlaskApplication().run()


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
        username=username,
        name=name,
        role=role
    )
    user.set_password(password)

    print("Do you want to add this user to the database?")
    print(user.dictionary)

    answers = inquirer.prompt([inquirer.Confirm("confirm", message="Confirm")])

    confirm = answers.get("confirm")
    if not confirm:
        return

    user.save()

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

import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.main import Application, db
import csv
from app.main.models.well import Well


app = Application(os.getenv("ENV") or "dev")

app.flask.app_context().push()

manager = Manager(app.flask)
migrate = Migrate(app.flask, db)


manager.add_command("db", MigrateCommand)


@manager.command
def run():
    app.flask.run(host="0.0.0.0", port=8080)


@manager.option('-h', '--host', dest='host', default='0.0.0.0')
@manager.option('-p', '--port', dest='port', type=int, default=8080)
@manager.option('-w', '--workers', dest='workers', type=int, default=4)
def run_prod(host, port, workers):
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
def test():
    """ Runs the unit tests """
    tests = unittest.TestLoader().discover("app/test", pattern="*_test.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()

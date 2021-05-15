"""
Created 10/03/2021
Prod Server WSGI Script
"""

from app.main import Application

app = Application("prod")
flask = app.flask


if __name__ == "__main__":
    flask.run()

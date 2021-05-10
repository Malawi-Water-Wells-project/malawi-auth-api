from app.main import Application


app = Application("prod")
flask = app.flask


if __name__ == "__main__":
    flask.run()

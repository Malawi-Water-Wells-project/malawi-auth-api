from flask import Flask, Blueprint
from .config import getConfig
from app.main.models.db import db
from flask_restx import Api


class Application():
    def __init__(self, config_name: str):
        self.config = getConfig(config_name)
        self.flask = Flask(__name__)
        self.flask.config.from_object(self.config)
        db.init_app(self.flask)

        self.blueprint = Blueprint("api", __name__)
        self.api = Api(self.blueprint, title="Malawi Auth API", version="1.0")

        self.flask.register_blueprint(self.blueprint)

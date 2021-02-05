from flask import Flask, Blueprint
from .config import getConfig
from flask_restx import Api
from .models import db
from app.main.controllers.tribe_controller import api as tribe_namespace
from app.main.controllers.auth_controller import api as auth_namespace


class Application():
    def __init__(self, config_name: str):
        self.config = getConfig(config_name)
        self.flask = Flask(__name__)
        self.flask.config.from_object(self.config)
        db.init_app(self.flask)

        blueprint = Blueprint("auth_api", __name__)
        self.api = Api(
            blueprint,
            title="Malawi Wells Authentication API",
            version="1.0"
        )

        self._bind_controllers()
        self.flask.register_blueprint(blueprint)

    def _bind_controllers(self):
        self.api.add_namespace(tribe_namespace, "/tribe")
        self.api.add_namespace(auth_namespace, "/auth")

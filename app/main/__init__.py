"""
Created 05/02/2021
"""
from app.main.config import get_config_for_env
from app.main.controllers import bind_controllers
from app.main.models import db
from dotenv import load_dotenv
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_restx import Api


class Application():
    """
    Root Application to bootstrap all other services
    """

    def __init__(self, config_name: str):
        load_dotenv()
        self.config = get_config_for_env(config_name)
        self.flask = Flask(__name__)
        self.flask.config.from_object(self.config)
        CORS(self.flask)
        db.init_app(self.flask)

        blueprint = Blueprint("auth_api", __name__,  url_prefix="/")
        self.api = Api(
            blueprint,
            title="Malawi Wells Authentication API",
            version="1.0",
            validate=False
        )

        bind_controllers(self.api)

        self.flask.register_blueprint(blueprint)

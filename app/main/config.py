"""
Created 05/02/2021
Application Config
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ Abstract Config Class """
    SECRET_KEY = os.environ.get("APP_SECRET_KEY", "Shhhhh")
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """ Config for a Development Environment """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/postgres"
    CORS_ALLOW_HEADERS = ["authorization", "content-type"]
    CORS_ORIGINS = ["admin.local.africawater.org"]


class TestingConfig(Config):
    """ Config for Testing Suites """
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, '../../tmp/devdb_test.db')}"


class ProductionConfig(Config):
    """ Production Config """

    def __init__(self):
        pg_user = os.getenv("POSTGRES_USER")
        pg_password = os.getenv("POSTGRES_PASSWORD")
        pg_host = os.getenv("POSTGRES_HOST")
        pg_db = os.getenv("POSTGRES_DATABASE")

        # pylint: disable=invalid-name
        self.SQLALCHEMY_DATABASE_URI = f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_db}"

    DEBUG = False


def get_config_for_env(env: str) -> Config:
    """ Returns the correct config for each environment """
    if env not in ["dev", "test", "prod"]:
        raise Exception("Invalid Environment")

    config = {
        "dev": DevelopmentConfig(),
        "test": TestingConfig(),
        "prod": ProductionConfig()
    }

    return config[env]


secret_key = Config.SECRET_KEY

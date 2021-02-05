import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    def __init__(self):
        load_dotenv()

    SECRET_KEY = os.getenv("SECRET_KEY", "shhhitsasecret")
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, '../../tmp/devdb_main.db')}"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, '../../tmp/devdb_test.db')}"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRES_URI")


def getConfig(env: str) -> Config:
    if env not in ["dev", "test", "prod"]:
        raise Exception("Invalid Environment")

    config = {
        "dev": DevelopmentConfig,
        "test": TestingConfig,
        "prod": ProductionConfig
    }
    return config[env]


secret_key = Config.SECRET_KEY

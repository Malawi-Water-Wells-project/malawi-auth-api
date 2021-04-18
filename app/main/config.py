import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = None
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
    def __init__(self):
        pg_user = os.getenv("POSTGRES_USER")
        pg_password = os.getenv("POSTGRES_PASSWORD")
        pg_host = os.getenv("POSTGRES_HOST")
        pg_db = os.getenv("POSTGRES_DATABASE")
        self.SQLALCHEMY_DATABASE_URI = f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_db}"

    DEBUG = False


def getConfig(env: str) -> Config:
    if env not in ["dev", "test", "prod"]:
        raise Exception("Invalid Environment")

    config = {
        "dev": DevelopmentConfig(),
        "test": TestingConfig(),
        "prod": ProductionConfig()
    }

    return config[env]


secret_key = Config.SECRET_KEY

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    def __init__(self):
        load_dotenv()

    SECRET_KEY = os.getenv("SECRET_KEY", "shhhitsasecret")
    DEBUG = False
    DATABASE_HOST = os.getenv("POSTGRES_USER")
    DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DATABASE_DB = os.getenv("POSTGRES_DB")
    DATABASE_PORT = os.getenv("POSTGRES_PORT")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


def getConfig(env: str):
    if env not in ["dev", "test", "prod"]:
        raise Exception("Invalid Environment")

    config = {
        "dev": DevelopmentConfig,
        "test": TestingConfig,
        "prod": ProductionConfig
    }
    return config[env]


secret_key = Config.SECRET_KEY

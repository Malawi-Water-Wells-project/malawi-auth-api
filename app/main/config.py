"""
Created 05/02/2021
Application Config
"""
#pylint: disable=too-few-public-methods

import os
basedir = os.path.abspath(os.path.dirname(__file__))
AW_ENV_NAME = os.environ["AW_ENV_NAME"].upper()


class Config:
    """ Abstract Config Class """
    SECRET_KEY = os.environ["APP_SECRET_KEY"]
    AW_ENV_NAME = AW_ENV_NAME
    AWS_REGION = os.environ["AWS_REGION"]
    DEBUG = False
    TESTING = False
    DYNAMODB_HOST = "http://localhost:8000" if AW_ENV_NAME == "LOCAL" else None

    class Tables:
        """ DynamoDB Tables """
        USERS = f"{AW_ENV_NAME}__Users"
        VILLAGES = f"{AW_ENV_NAME}__Villages"
        REFRESH_TOKENS = f"{AW_ENV_NAME}__RefreshTokens"
        JOIN_TOKENS = f"{AW_ENV_NAME}__JoinTokens"
        WELLS = f"{AW_ENV_NAME}__Wells"


class DevelopmentConfig(Config):
    """ Config for a Development Environment """
    DEBUG = True
    CORS_ALLOW_HEADERS = ["authorization", "content-type"]
    CORS_ORIGINS = ["admin.local.africawater.org"]


class LocalConfig(DevelopmentConfig):
    """ Config for a Local Dev Environment """
    DYNAMODB_HOST = "http://localhost:8000"


class TestingConfig(Config):
    """ Config for Testing Suites """
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """ Production Config """
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

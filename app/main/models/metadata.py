"""
Created 17/07/2021
Default Metadata for DynamoDB Tables
"""

from app.main.config import Config


class DefaultMeta:
    """ Default Table Metadata """
    region = Config.AWS_REGION
    host = Config.DYNAMODB_HOST
    read_capacity_units = 5 if Config.AW_ENV_NAME == "LOCAL" else None
    write_capacity_units = 5 if Config.AW_ENV_NAME == "LOCAL" else None

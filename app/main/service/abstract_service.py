"""
Created 25/05/2021
"""
from app.main.models import db
import redis
from typing import Type
import os


class AbstractService:
    MODEL = None

    @classmethod
    def get_by_id(cls, id: int):
        """
        Gets the model by ID
        """
        return cls.filter(id=id).first()

    @classmethod
    def model(cls):
        assert cls.MODEL is not None
        return cls.MODEL

    @classmethod
    def filter(cls, **kwargs):
        return cls.model().query.filter_by(**kwargs)


class AbstractRedisService(AbstractService):
    REDIS_DB = 0
    _redisClient = None

    @classmethod
    def redisClient(cls) -> Type[redis.Redis]:
        if cls._redisClient is None:
            cls._redisClient = redis.Redis(host=os.environ.get("REDIS_HOST"),
                                           port=os.environ.get("REDIS_PORT"),
                                           db=0)
        return cls._redisClient

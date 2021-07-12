"""
Created 20/05/2021
Logging Util
"""
import logging
import os
from configparser import ConfigParser

from dotenv import load_dotenv
from flask import has_request_context, request

LOG_CACHE = ConfigParser()


class AppLogger():
    """ Application Logger """
    _LOG_CAST = {
        "FATAL": logging.FATAL,
        "ERROR": logging.ERROR,
        "WARN": logging.WARN,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG
    }

    def __init__(self, log_level=logging.DEBUG):
        self.log_level = log_level
        self._logger = logging.getLogger("malawi-auth-api")
        self._logger.setLevel(log_level)

        if not self._logger.hasHandlers():
            self._bind_handlers()

        if len(LOG_CACHE) == 1:
            self._load_log_cache()

    def _bind_handlers(self):
        """ Binds Logstash Handlers to the Logging object """
        load_dotenv()
        handler = logging.StreamHandler()
        handler.setLevel(self.log_level)

    def log(self, log_point: str, data: dict = None):
        """ Logs the current logpoint """
        if not LOG_CACHE.has_section(log_point):
            raise ValueError(f"Log Point {log_point} has not been defined")

        level = LOG_CACHE[log_point].get("LogLevel")
        text = LOG_CACHE[log_point].get("LogText")

        if not level or not text:
            raise ValueError(
                f"Log Point {log_point} is missing one or both of LogLevel and LogText")

        casted_level = self._cast_log_level(level)
        extra = {
            "code": log_point,
            **(data or {})
        }

        if has_request_context():
            extra.update({"internal_id": request.view_args.get("internal_id")})

        self._logger.log(casted_level, text, extra=extra)

    def log_crash(self, code):
        pass

    @classmethod
    def _cast_log_level(cls, level: str) -> int:
        """ Casts the string log level to the Python logger levels """
        casted_level = cls._LOG_CAST.get(level)
        if casted_level is None:
            raise ValueError(f"Log Level {level} improperly defined")
        return casted_level

    def _load_log_cache(self):
        assert os.path.exists(
            "app/config/logpoints.ini"), "logpoints.ini not found"
        LOG_CACHE.read("app/config/logpoints.ini")
        assert len(LOG_CACHE) > 1

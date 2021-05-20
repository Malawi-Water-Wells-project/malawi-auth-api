"""
Created 20/05/2021
Logging Util
"""
import logging
import os
from logstash_async.handler import AsynchronousLogstashHandler


Logger = None  # pylint: disable=invalid-name

logger = logging.getLogger("python-logstash-logger")
logger.setLevel(logging.DEBUG)
handler = AsynchronousLogstashHandler(
    host=os.environ["host"], port=os.environ["port"], database_path=None)
logger.addHandler(handler)


def get_logger():
    if logger is None:
        init_logger()
    return logger

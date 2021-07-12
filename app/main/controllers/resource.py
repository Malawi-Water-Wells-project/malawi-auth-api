"""
Created 15/05/2021
Abstract API Resource
"""
from datetime import date, datetime
from sys import intern
from uuid import uuid4

from app.main.constants import ResponseStatus
from app.main.util.logger import AppLogger
from flask import has_request_context, request
from flask_restx import Resource as FlaskResource


class Resource(FlaskResource):
    """ Abstract Resource for Handlers """

    def __init__(self, api, *args, **kwargs):
        super().__init__(api=api, *args, **kwargs)
        self.logger = AppLogger()
        self._start_time = None

        internal_id = str(uuid4())
        self.internal_id = internal_id
        if has_request_context():
            request.view_args["internal_id"] = internal_id

    @staticmethod
    def _build_response(code: int, status: str, data: dict = None):
        """ Formats a response into a consistent format """
        if data is None:
            data = {}

        return {"code": code, "status": status, **data}, code

    @staticmethod
    def format_success(code: int, data: dict = None):
        """ Formats a success response into a consistent format """
        return Resource._build_response(code, ResponseStatus.SUCCESS, data)

    @staticmethod
    def format_failure(code: int, error: str, data: dict = None):
        """ Formats a failure response into a consistent format """
        if data is None:
            data = {"error": error}
        else:
            data.update({"error": error})

        return Resource._build_response(code, ResponseStatus.FAILURE, data)

    @staticmethod
    def format_mixed(code: int, error: str, data: dict = None):
        """ Formats a custom response into a consistent format """
        if data is None:
            data = {"error": error}
        else:
            data.update({"error": error})

        return Resource._build_response(code, ResponseStatus.MIXED, data)

    @staticmethod
    def no_permissions_for_action():
        """ Returns an access denied response for an action """
        return Resource.format_failure(403, "You are not authorized to perform this action.")

    def dispatch_request(self, *args, **kwargs):
        self._log_request()
        try:
            response, code = super().dispatch_request(*args, **kwargs)
            self._log_response(response, code)
            return response, code
        except Exception as exc:  # pylint: disable=broad-except
            self._log_failure(exc)
            return self.format_failure(500, "Internal Server Error")

    @property
    def _current_time(self) -> float:
        """ Returns the current time as a timestamp """
        return datetime.now().timestamp()

    def _log_request(self):
        self._start_time = self._current_time
        self.logger.log("FLASK000")

    def _log_response(self, response: dict, code: int):
        response_time = self._current_time - self._start_time
        self.logger.log("FLASK999", {
            "response_time": round(response_time, 5),
            "response_code": code
        })

    def _log_failure(self, exception):
        # exc_info = sys.exc_info()
        self.logger.log("FLASK001", {
            "exception": str(exception),
        })

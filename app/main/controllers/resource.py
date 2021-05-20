"""
Created 15/05/2021
Abstract API Resource
"""
from app.main.constants import ResponseStatus
from flask.wrappers import Response
from flask_restx import Resource as FlaskResource


class Resource(FlaskResource):
    """ Abstract Resource for Handlers """
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

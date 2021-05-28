"""
Created 20/05/2021
Abstract Request Validator
"""
from abc import ABCMeta

from cerberus import Validator as CerberusValidator
from flask import request
from werkzeug.datastructures import EnvironHeaders


class StopValidationException(Exception):
    """ Stops the validation and returns the response to the client """


class LookupCache(dict):
    """ A cache for DB lookups performed during validation """

    def add(self, key: str, value):
        """ Adds an entry to the cache """
        self.update({key: value})


class AbstractRequestValidator(metaclass=ABCMeta):
    """
    Implements methods and validation lifecycle to be
    used by child classes
    """
    SCHEMA: dict = None
    RUN_SCHEMA_CHECK = True

    def __init__(self):
        self._errors = []
        self.lookup_cache = LookupCache()

    def add_error(self, topic: str, error: str):
        """ Add an error into the internal list of errors """
        self._errors.append(f"{topic}: {error}")

    def validate(self):
        """ Run the validation lifecycle and allow halting of validation """
        try:
            self._run_lifecycle()
        except StopValidationException:
            return

    def _run_lifecycle(self):
        """ Runs the validation """
        self.prevalidation()
        if not self.is_valid:
            raise StopValidationException("Prevalidation Failed")

        self.validate_headers(request.headers)
        if not self.is_valid:
            raise StopValidationException("Header Validation Failed")

        self._run_body_validation()
        if not self.is_valid:
            raise StopValidationException("Body Validation Failed")

        self.postvalidation()
        if not self.is_valid:
            raise StopValidationException("Postvalidation Failed")

    def _run_body_validation(self):
        """ Runs the schema check if needed, and body validation function """
        if self.RUN_SCHEMA_CHECK:
            self._run_cerberus()
            if not self.is_valid:
                return

        self.validate_body(request.json)

    def _run_cerberus(self):
        """ Runs the Cerberus validator with the schema """
        if not self.SCHEMA:
            raise ValueError("SCHEMA not set")

        validator = CerberusValidator(self.SCHEMA)
        validator.validate(request.json)

        for key in validator.errors:
            for error in validator.errors[key]:
                self.add_error(key, error)

    @property
    def is_valid(self) -> bool:
        """ Returns whether validation errors exist """
        print(self._errors)
        return len(self._errors) == 0

    def prevalidation(self):
        """
        The first validation checks, runs before all others.
        To be implemented by child classes
        """

    def validate_headers(self, headers: EnvironHeaders):
        """ To be implemented by child classes """

    def validate_body(self, body: dict):
        """ To be implemented by child classes """

    def postvalidation(self):
        """
        The last validation checks, runs after all others.
        To be implemented by child classes
        """

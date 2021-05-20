"""
Created 20/05/2021
Validation Decorators
"""
from functools import wraps

from app.main.controllers.resource import Resource
from app.main.util.validation.requests.abstract_request_validator import \
    AbstractRequestValidator
from flask.globals import request


#pylint: disable=invalid-name
def validate(Validator: AbstractRequestValidator):
    """ Decorator for validating an incoming request with a validator """
    def decorator(wrapped_func):
        @wraps(wrapped_func)
        def wrapper(*args, **kwargs):
            validator = Validator()
            errors = validator.validate()

            if not validator.is_valid:
                return Resource.format_failure(
                    400,
                    "There were validation errors in your request",
                    {"validation_errors": errors}
                )

            return wrapped_func(*args, **kwargs, **validator.lookup_cache, body=request.json)

        return wrapper
    return decorator

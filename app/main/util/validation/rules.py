"""
Created 20/05/2021
Common Validation Rules
"""
from app.main.constants import UserRoles


class Rule(dict):
    """ A dictionary based rule """

    def extend(self, **kwargs):
        """ Extends upon the existing rule """
        return {**self, **kwargs}

    @property
    def required(self):
        """ Adds the required parameter to the rule """
        return Rule({
            **self,
            "required": True
        })


class CommonRules:
    """ Common Cerberus Validation Rules """

    NAME = Rule({
        "type": "string",
        "empty": False
    })
    USERNAME = Rule({
        "type": "string",
        "maxlength": 50,
        "empty": False,
        "regex": "^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$"
    })
    PASSWORD = Rule({
        "type": "string",
        "minlength": 6,
        "empty": False
    })
    TRIBE_ID = Rule({
        "type": "string",
        "empty": False,
        "regex": "[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$"
    })
    TOKEN = Rule({
        "type": "string",
        "empty": False,
        "regex": "[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$"
    })
    ROLE = Rule({
        "type": "string",
        "empty": False,
        "allowed": [UserRoles.ADMIN, UserRoles.TRIBE_ADMIN, UserRoles.USER]
    })
    FLOAT = Rule({
        "type": "number",
        "empty": False
    })
    STRING = Rule({
        "type": "string",
        "empty": False
    })

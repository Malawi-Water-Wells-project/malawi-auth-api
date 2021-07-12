"""
Created 13/06/2021
Integration Test Constants
"""


API_ENDPOINT_URL = "http://localhost:8080"


class ResponseStatus:
    SUCCESS = "Success"


INTEGRATION_TEST_PASSWORD = "inttestpassword"


class TestLogins:
    """
    Logins for the Integration Test framework
    """
    ADMIN = {
        "username": "inttest-admin",
        "password": INTEGRATION_TEST_PASSWORD
    }

    VILLAGEADMIN = {
        "username": "inttest-villageadmin",
        "password": INTEGRATION_TEST_PASSWORD
    }

    USER = {
        "username": "inttest-user",
        "password": INTEGRATION_TEST_PASSWORD
    }

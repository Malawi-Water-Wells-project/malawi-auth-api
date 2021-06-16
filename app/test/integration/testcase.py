"""
Created 16/06/2021
Abstract TestCase
"""
from app.test.integration.constants import API_ENDPOINT_URL
import unittest
import requests
from typing import Tuple


class IntegrationTestCase(unittest.TestCase):
    """ Abstract Integration Test Case """
    _tokens = {}

    def get_tokens(self, user: dict) -> Tuple[str, str]:
        """ Gets JWT Tokens from the API """

        response = requests.post(f"{API_ENDPOINT_URL}/auth/login", json=user)
        assert response.status_code == 200

        body = response.json()

        return body["tokens"]["access"], body["tokens"]["refresh"]

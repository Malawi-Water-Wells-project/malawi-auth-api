"""
Created 13/06/2021
Integration Tests for /auth/login
"""
from datetime import datetime
from unittest import TestCase
from app.test.integration.constants import API_ENDPOINT_URL, ResponseStatus, TestLogins
from app.test.integration.testcase import IntegrationTestCase
from datetime import timedelta
import requests
import jwt


class LoginTests(IntegrationTestCase):
    """
    Test Cases for /auth/login
    """

    def test_login_as_admin(self):
        """ Test """

        # Login with Admin Test User
        response = requests.post(
            f"{API_ENDPOINT_URL}/auth/login", json=TestLogins.ADMIN)

        # Assert that we got a 200 response
        self.assertEqual(response.status_code, 200)

        response_body = response.json()

        # Body Assertions
        self.assertEqual(response_body["status"], ResponseStatus.SUCCESS)
        self.assertIsInstance(response_body["user"], dict)
        self.assertEqual(response_body["user"]
                         ["name"], "Integration Test Admin")
        self.assertEqual(response_body["user"]["role"], "admin")

        # JWT Assertions
        access_token = jwt.decode(
            response_body["tokens"]["access"],
            "",
            algorithms=["HS256"],
            options={"verify_signature": False}
        )

        self.assertEqual(access_token["user_id"],
                         response_body["user"]["user_id"])
        self.assertEqual(access_token["role"], "admin")

        # Access Token should expire 15 minutes after creation - allow 5 seconds either way
        actual_expiry = access_token["exp"]
        self.assertIsNotNone(actual_expiry)

        expected_expiry = datetime.now() + timedelta(minutes=15)

        self.assertLess(actual_expiry, expected_expiry.timestamp() + 5)
        self.assertGreater(actual_expiry, expected_expiry.timestamp() - 5)

        refresh_token = jwt.decode(
            response_body["tokens"]["refresh"],
            "",
            algorithms=["HS256"],
            options={"verify_signature": False}
        )

        self.assertEqual(access_token["user_id"],
                         response_body["user"]["user_id"])
        self.assertEqual(access_token["role"], "admin")

        # Refresh Token should expire 52 weeks after creation - allow 5 seconds either way
        actual_expiry = refresh_token["exp"]
        self.assertIsNotNone(actual_expiry)

        expected_expiry = datetime.now() + timedelta(weeks=52)

        self.assertLess(actual_expiry, expected_expiry.timestamp() + 5)
        self.assertGreater(actual_expiry, expected_expiry.timestamp() - 5)

"""
Created 16/06/2021
Tests for /users/current
"""

from app.test.integration.constants import API_ENDPOINT_URL, TestLogins
import requests
from app.test.integration.testcase import IntegrationTestCase


class CurrentUserTestCase(IntegrationTestCase):
    """
    Tests for /users/current
    """

    def test_not_logged_in(self):
        """ Test that an error is returned when not logged in """
        response = requests.get(f"{API_ENDPOINT_URL}/users/current")

        self.assertEqual(response.status_code, 401)

        body = response.json()
        self.assertEqual(body, {
            "status": "Failure",
            "code": 401,
            "error": "Not Authorized"
        })

    def test_admin_logged_in(self):
        """ Test that it works correctly with an admin """
        token, _ = self.get_tokens(TestLogins.ADMIN)

        response = requests.get(
            f"{API_ENDPOINT_URL}/users/current", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertEqual(body["status"], "Success")
        self.assertEqual(body["code"], 200)

        self.assertEqual(body["user"]["name"], "Integration Test Admin")
        self.assertEqual(body["user"]["role"], "admin")

    def test_village_admin_logged_in(self):
        """ Test that it works correctly with a villageadmin """
        token, _ = self.get_tokens(TestLogins.VILLAGEADMIN)

        response = requests.get(
            f"{API_ENDPOINT_URL}/users/current", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertEqual(body["status"], "Success")
        self.assertEqual(body["code"], 200)

        self.assertEqual(body["user"]["name"], "Integration Test VillageAdmin")
        self.assertEqual(body["user"]["role"], "villageadmin")

    def test_user_logged_in(self):
        """ Test that it works correctly with a user """
        token, _ = self.get_tokens(TestLogins.USER)

        response = requests.get(
            f"{API_ENDPOINT_URL}/users/current", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertEqual(body["status"], "Success")
        self.assertEqual(body["code"], 200)

        self.assertEqual(body["user"]["name"], "Integration Test User")
        self.assertEqual(body["user"]["role"], "user")

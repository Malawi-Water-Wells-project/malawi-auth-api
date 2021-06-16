"""
Create 13/06/2021
Tests for /users/create
"""

from app.test.integration.testcase import IntegrationTestCase
import requests
from app.test.integration.constants import API_ENDPOINT_URL, ResponseStatus, TestLogins, INTEGRATION_TEST_PASSWORD
from parameterized import parameterized


class CreateUserTests(IntegrationTestCase):
    """
    Tests for /users/create
    """

    def test_happy_path(self):
        """ Test User Creation Happy Path """
        # Get Admin Tokens
        token, _ = self.get_tokens(TestLogins.ADMIN)

        # Create a new User
        new_user = {
            "username": "MrTestUser",
            "password": "MrTestUserPass",
            "name": "Mr Test User"
        }

        response = requests.post(
            f"{API_ENDPOINT_URL}/users/create",
            json=new_user,
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 201)

        body = response.json()

        user_id = body["user"]["user_id"]
        self.addCleanup(lambda: self._remove_user(user_id))

        # Body Assertions
        self.assertEqual(body["status"], ResponseStatus.SUCCESS)
        self.assertEqual(body["user"]["role"], "user")
        self.assertEqual(body["user"]["username"], "MrTestUser")
        self.assertEqual(body["user"]["name"], "Mr Test User")
        self.assertIsNone(body["user"].get("password"))

        # Check that new user can login
        response = requests.post(f"{API_ENDPOINT_URL}/auth/login",
                                 json={"username": "MrTestUser", "password": "MrTestUserPass"})
        self.assertEqual(response.status_code, 200)

        body = response.json()

        self.assertEqual(body["status"], ResponseStatus.SUCCESS)
        self.assertEqual(body["user"]["user_id"], user_id)

    @parameterized.expand([[TestLogins.USER], [TestLogins.TRIBEADMIN]])
    def test_create_user_other_roles(self, role):
        """
        Test that a user with role "user" or "tribeadmin" cannot create another user
        """
        token, _ = self.get_tokens(role)

        response = requests.post(
            f"{API_ENDPOINT_URL}/users/create", headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 403)
        body = response.json()

        self.assertEqual(body["code"], 403)
        self.assertEqual(body["status"], "Failure")
        self.assertEqual(
            body["error"], "You are not authorized to perform this action.")

    def test_create_user_with_tribe(self):
        """
        Test that a user can be created and associated with a tribe
        """
        token, _ = self.get_tokens(TestLogins.ADMIN)

        new_user = {
            "username": "MrTestUser",
            "password": "MrTestUserPass",
            "name": "Mr Test User",
            "tribe_id": "e035ac48-872c-4f78-a092-cbfb34f888ec"
        }

        response = requests.post(f"{API_ENDPOINT_URL}/users/create",
                                 json=new_user, headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(response.status_code, 201)
        body = response.json()
        user_id = body["user"]["user_id"]

        self.addCleanup(lambda: self._remove_user(user_id))

        self.assertEqual(body["user"]["tribe_id"],
                         "e035ac48-872c-4f78-a092-cbfb34f888ec")

        # Get Tribe
        response = requests.get(
            f"{API_ENDPOINT_URL}/tribes/e035ac48-872c-4f78-a092-cbfb34f888ec")

        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertIn(user_id, body["tribe"]["users"])

    def _remove_user(self, user_id: str):
        """ Cleanup - Removes the created user """
        response = requests.delete(f"{API_ENDPOINT_URL}/users/{user_id}")
        assert response.status_code == 204

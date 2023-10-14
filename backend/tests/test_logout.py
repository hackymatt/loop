from rest_framework import status
from rest_framework.test import APITestCase
from .factory import create_user
from django.contrib import auth
from .helpers import login


class LogoutTest(APITestCase):
    def setUp(self):
        self.endpoint = "/logout"
        self.data = {"email": "email@example.com", "password": "test_password"}
        create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )

    def test_logout_if_not_loggedin(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        data = {"email": self.data["email"]}
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_logout_if_loggedin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # logout
        data = {"email": self.data["email"]}
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

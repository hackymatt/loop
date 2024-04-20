from rest_framework import status
from rest_framework.test import APITestCase
from .factory import create_user, create_profile
from .helpers import (
    users_number,
    login,
    is_user_found,
    profiles_number,
)
from django.contrib import auth


class UnregisterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/unregister"
        self.data = {
            "email": "test_email@example.com",
            "password": "TestPassword123",
        }
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.profile = create_profile(user=self.user)

    def test_delete_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # delete
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(is_user_found(self.data["email"]))
        self.assertEqual(profiles_number(), 2)
        self.assertEqual(users_number(), 2)

    def test_delete_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(is_user_found(self.data["email"]))
        self.assertEqual(profiles_number(), 1)
        self.assertEqual(users_number(), 1)

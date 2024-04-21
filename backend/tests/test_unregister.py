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
        self.admin_data = {
            "email": "admin_test_email@example.com",
            "password": "TestPassword123",
        }
        self.admin_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.admin_data["email"],
            password=self.admin_data["password"],
            is_active=True,
            is_staff=True,
        )
        self.admin_profile = create_profile(user=self.admin_user, user_type="A")
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
        self.lecturer_data = {
            "email": "lecturer_1@example.com",
            "password": "TestPassword123",
        }
        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.lecturer_data["email"],
            password=self.lecturer_data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_profile(user=self.lecturer_user, user_type="W")

    def test_delete_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # delete
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(is_user_found(self.data["email"]))
        self.assertEqual(profiles_number(), 6)
        self.assertEqual(users_number(), 6)

    def test_delete_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(is_user_found(self.admin_data["email"]))
        self.assertEqual(profiles_number(), 6)
        self.assertEqual(users_number(), 6)

    def test_delete_authenticated_lecturer(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(is_user_found(self.lecturer_data["email"]))
        self.assertEqual(profiles_number(), 5)
        self.assertEqual(users_number(), 5)

    def test_delete_authenticated_student(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(is_user_found(self.data["email"]))
        self.assertEqual(profiles_number(), 5)
        self.assertEqual(users_number(), 5)

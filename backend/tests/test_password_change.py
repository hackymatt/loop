from rest_framework import status
from rest_framework.test import APITestCase
from .factory import create_user
from .helpers import login
from django.contrib import auth


class PasswordChangeTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/password-change"
        self.data = {"email": "email@example.com", "password": "TestPassword1234!"}
        create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )

    def test_old_password_new_password_match(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # old password and new password ARE the same
        data = {
            "old_password": self.data["password"],
            "password": self.data["password"],
            "password2": self.data["password"],
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            auth.get_user(self.client).check_password(self.data["password"])
        )

    def test_password_strength(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new password with less than 8 characters
        new_password = "abcd"
        data = {
            "old_password": self.data["password"],
            "password": new_password,
            "password2": new_password,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            auth.get_user(self.client).check_password(self.data["password"])
        )

        # new password without numbers and uppercase letter
        new_password = "abcdefghi"
        data = {
            "old_password": self.data["password"],
            "password": new_password,
            "password2": new_password,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            auth.get_user(self.client).check_password(self.data["password"])
        )

        # new password without uppercase letter
        new_password = "abcde1234"
        data = {
            "old_password": self.data["password"],
            "password": new_password,
            "password2": new_password,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            auth.get_user(self.client).check_password(self.data["password"])
        )

    def test_new_password_match(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new password and password 2 does not match
        new_password = "TestPassword123"
        new_password_2 = "TestPassword1234"
        data = {
            "old_password": self.data["password"],
            "password": new_password,
            "password2": new_password_2,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            auth.get_user(self.client).check_password(self.data["password"])
        )

    def test_unauthenticated_user(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # new password
        new_password = "TestPassword123"
        data = {
            "old_password": self.data["password"],
            "password": new_password,
            "password2": new_password,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(
            auth.get_user(self.client).check_password(self.data["password"])
        )

    def test_current_password_mismatch(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new password
        old_password = self.data["password"] + "1"
        new_password = "TestPassword123!"
        data = {
            "old_password": old_password,
            "password": new_password,
            "password2": new_password,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(
            auth.get_user(self.client).check_password(self.data["password"])
        )

    def test_password_change_success(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new password
        new_password = "TestPassword123!"
        data = {
            "old_password": self.data["password"],
            "password": new_password,
            "password2": new_password,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        login(self, self.data["email"], new_password)
        self.assertFalse(
            auth.get_user(self.client).check_password(self.data["password"])
        )

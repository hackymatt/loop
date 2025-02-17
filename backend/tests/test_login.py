from rest_framework import status
from rest_framework.test import APITestCase
from .factory import create_user, create_profile
from django.contrib import auth
from const import UserType


class LoginTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/login"
        self.data_1 = {"email": "email@example.com", "password": "test_password"}
        self.user1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data_1["email"],
            password=self.data_1["password"],
            is_active=True,
        )
        create_profile(user=self.user1)

        self.data_2 = {"email": "email_2@example.com", "password": "test_password_2"}
        self.user2 = create_user(
            first_name="first_name_2",
            last_name="last_name_2",
            email=self.data_2["email"],
            password=self.data_2["password"],
            is_active=False,
        )
        create_profile(user=self.user2, user_type=UserType.INSTRUCTOR)

    def test_login_correct_credentials_1(self):
        response = self.client.post(self.endpoint, self.data_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(auth.get_user(self.client).is_authenticated)

    def test_login_correct_credentials_2(self):
        self.user2.is_active = True
        self.user2.save()
        response = self.client.post(self.endpoint, self.data_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(auth.get_user(self.client).is_authenticated)

    def test_login_incorrect_email(self):
        response = self.client.post(
            self.endpoint,
            {"email": "incorrect@example.com", "password": self.data_1["password"]},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_login_incorrect_password(self):
        response = self.client.post(
            self.endpoint,
            {"email": self.data_1["email"], "password": "incorrect_password"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_login_incorrect_credentials(self):
        response = self.client.post(
            self.endpoint,
            {"email": "incorrect@example.com", "password": "incorrect_password"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

    def test_login_inactive_user(self):
        response = self.client.post(self.endpoint, self.data_2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(auth.get_user(self.client).is_authenticated)

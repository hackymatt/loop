from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from unittest.mock import patch
from .factory import create_user, create_profile, create_student_profile
from .helpers import login, mock_send_message
from django.contrib import auth
from utils.google.gmail import GmailApi


class PasswordResetTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/password-reset"
        self.client = APIClient()
        self.data = {"email": "email@example.com", "password": "test_password"}
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.profile = create_student_profile(profile=create_profile(user=self.user))

    @patch.object(GmailApi, "_send_message")
    def test_incorrect_email(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # password reset request
        data = {"email": "email_2@example.com"}
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(
            auth.get_user(self.client).check_password(self.data["password"])
        )
        self.assertEqual(_send_message_mock.call_count, 0)

    @patch.object(GmailApi, "_send_message")
    def test_password_reset_success(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # password reset request
        data = {"email": self.data["email"]}
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        login(self, self.data["email"], self.data["password"])
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.assertEqual(_send_message_mock.call_count, 1)

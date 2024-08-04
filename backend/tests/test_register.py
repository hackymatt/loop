from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from unittest.mock import patch
from .factory import create_user, create_newsletter
from .helpers import (
    users_number,
    is_user_found,
    get_user,
    profiles_number,
    is_profile_found,
    get_profile,
    is_data_match,
    mock_send_message,
    newsletters_number,
)
from utils.google.gmail import GmailApi


class RegisterTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/register"
        self.client = APIClient()
        self.data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test_email@example.com",
            "password": "TestPassword123!",
            "password2": "TestPassword123!",
        }
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="email@example.com",
            password="password",
            is_active=True,
        )

    @patch.object(GmailApi, "_send_message")
    def test_incorrect_email(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        data = self.data.copy()
        data["email"] = "email@example.com"
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 4)
        self.assertEqual(_send_message_mock.call_count, 0)
        self.assertEqual(newsletters_number(), 0)

    @patch.object(GmailApi, "_send_message")
    def test_password_strength(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # new password with less than 8 characters
        new_password = "abcd"
        data = self.data.copy()
        data["password"] = new_password
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 4)
        self.assertEqual(_send_message_mock.call_count, 0)
        self.assertEqual(newsletters_number(), 0)

        # new password without numbers
        new_password = "testpassword"
        data = self.data.copy()
        data["password"] = new_password
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 4)
        self.assertEqual(_send_message_mock.call_count, 0)
        self.assertEqual(newsletters_number(), 0)

        # new password without uppercase letter
        new_password = "abcde1234"
        data = self.data.copy()
        data["password"] = new_password
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 4)
        self.assertEqual(_send_message_mock.call_count, 0)
        self.assertEqual(newsletters_number(), 0)

        # new password without lowercase letter
        new_password = "ABCDE1234"
        data = self.data.copy()
        data["password"] = new_password
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 4)
        self.assertEqual(_send_message_mock.call_count, 0)
        self.assertEqual(newsletters_number(), 0)

        # new password without special character
        new_password = "Abcde1234"
        data = self.data.copy()
        data["password"] = new_password
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 4)
        self.assertEqual(_send_message_mock.call_count, 0)
        self.assertEqual(newsletters_number(), 0)

    @patch.object(GmailApi, "_send_message")
    def test_new_password_match(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # new password and password 2 does not match
        new_password_2 = "TestPassword12345!"
        data = self.data.copy()
        data["password2"] = new_password_2
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 4)
        self.assertEqual(_send_message_mock.call_count, 0)
        self.assertEqual(newsletters_number(), 0)

    @patch.object(GmailApi, "_send_message")
    def test_register_success_without_newsletter(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(users_number(), 5)
        self.assertEqual(profiles_number(), 4)
        self.assertTrue(is_user_found(self.data["email"]))

        user = get_user(self.data["email"])
        profile = get_profile(user)

        self.assertTrue(is_profile_found(user))

        user_data = {
            "first_name": self.data["first_name"],
            "last_name": self.data["last_name"],
            "username": self.data["email"],
            "email": self.data["email"],
            "is_active": False,
        }

        self.assertTrue(is_data_match(user, user_data))
        self.assertNotEqual(user.password, None)
        self.assertTrue(user.check_password(self.data["password"]))
        self.assertNotEqual(profile.verification_code, None)
        self.assertNotEqual(profile.verification_code_created_at, None)
        self.assertEqual(_send_message_mock.call_count, 1)

        self.assertEqual(newsletters_number(), 1)

    @patch.object(GmailApi, "_send_message")
    def test_register_success_with_newsletter(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        create_newsletter(email=self.data["email"], active=False)
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(users_number(), 5)
        self.assertEqual(profiles_number(), 4)
        self.assertTrue(is_user_found(self.data["email"]))

        user = get_user(self.data["email"])
        profile = get_profile(user)

        self.assertTrue(is_profile_found(user))

        user_data = {
            "first_name": self.data["first_name"],
            "last_name": self.data["last_name"],
            "username": self.data["email"],
            "email": self.data["email"],
            "is_active": False,
        }

        self.assertTrue(is_data_match(user, user_data))
        self.assertNotEqual(user.password, None)
        self.assertTrue(user.check_password(self.data["password"]))
        self.assertNotEqual(profile.verification_code, None)
        self.assertNotEqual(profile.verification_code_created_at, None)
        self.assertEqual(_send_message_mock.call_count, 1)
        self.assertEqual(newsletters_number(), 1)

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from unittest.mock import patch
from .factory import (
    create_user,
    create_profile,
)
from .helpers import users_number, get_user, mock_send_message, get_profile
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from utils.google.gmail import GmailApi


class VerifyTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/verify"
        self.data_1 = {
            "email": "test_email@example.com",
            "code": "code1234",
        }
        self.user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data_1["email"],
            password="password",
            is_active=False,
        )
        self.profile_1 = create_profile(
            user=self.user_1,
            verification_code=self.data_1["code"],
        )
        self.data_2 = {
            "email": "test_email_2@example.com",
            "code": "code2222",
        }
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data_2["email"],
            password="password",
            is_active=True,
        )
        self.profile_2 = create_profile(
            user=self.user_2, verification_code=self.data_2["code"]
        )

    def test_incorrect_email(self):
        data = self.data_1.copy()
        data["email"] = "email@example.com"
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(users_number(), 5)

    def test_active_user(self):
        response = self.client.post(self.endpoint, self.data_2)
        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)
        self.assertEqual(users_number(), 5)
        self.assertTrue(self.user_2.is_active)

    def test_code_expiration(self):
        self.profile_1.verification_code_created_at = make_aware(
            datetime.now() - timedelta(days=1)
        )
        self.profile_1.save()
        response = self.client.post(self.endpoint, self.data_1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 5)
        self.assertFalse(self.user_1.is_active)

    def test_incorrect_code(self):
        data = self.data_1.copy()
        data["code"] = "code4567"
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 5)
        self.assertFalse(self.user_1.is_active)

    def test_verify_success(self):
        response = self.client.post(self.endpoint, self.data_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(users_number(), 5)
        self.assertTrue(get_user(self.data_1["email"]).is_active)


class VerificationCodeTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/verify-code"
        self.client = APIClient()
        self.data = {"email": "test_email@example.com"}
        self.verification_code = {
            "verification_code": "abcd1234",
            "verification_code_created_at": make_aware(
                datetime.now() - timedelta(days=12)
            ),
        }
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password="password",
            is_active=False,
        )
        self.profile = create_profile(
            user=self.user,
            verification_code=self.verification_code["verification_code"],
            verification_code_created_at=self.verification_code[
                "verification_code_created_at"
            ],
        )

    @patch.object(GmailApi, "_send_message")
    def test_incorrect_email(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        data = self.data.copy()
        data["email"] = "email@example.com"
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(_send_message_mock.call_count, 0)

    @patch.object(GmailApi, "_send_message")
    def test_verification_code_success(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(
            get_profile(self.user).verification_code,
            self.verification_code["verification_code"],
        )
        self.assertNotEqual(
            get_profile(self.user).verification_code_created_at,
            self.verification_code["verification_code_created_at"],
        )
        self.assertEqual(_send_message_mock.call_count, 1)

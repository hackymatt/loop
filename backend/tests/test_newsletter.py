from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from unittest.mock import patch
from .factory import (
    create_user,
    create_profile,
    create_admin_profile,
    create_student_profile,
    create_newsletter,
)
from .helpers import (
    login,
    newsletters_number,
    get_newsletter,
    is_data_match,
    mock_send_message,
)
from django.contrib import auth
import json
from utils.google.gmail import GmailApi


class NewsletterEntriesTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/newsletter"

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
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )

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
        self.profile = create_student_profile(profile=create_profile(user=self.user))

        self.active_newsletters = [
            create_newsletter(email=f"test_active_{i}@example.com") for i in range(15)
        ]
        self.inactive_newsletters = [
            create_newsletter(email=f"test_inactive_{i}@example.com", active=False)
            for i in range(5)
        ]

    def test_get_newsletter_entries_unauthenticated(self):
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_newsletter_entries_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_newsletter_entries_success(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 20)

    def test_get_newsletter_entry_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.active_newsletters[0].id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_newsletter_entry_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.active_newsletters[0].id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_newsletter_entry_success(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.active_newsletters[0].id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        newsletter = get_newsletter(uuid=self.active_newsletters[0].uuid)
        self.assertTrue(is_data_match(newsletter, data))


class NewsletterSubscribeTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/newsletter-subscribe"
        self.client = APIClient()

    @patch.object(GmailApi, "_send_message")
    def test_subscribe_to_newsletter_without_history(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # post data
        data = {"email": "test@example.com"}
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(newsletters_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)

    @patch.object(GmailApi, "_send_message")
    def test_subscribe_to_newsletter_with_history_inactive(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        data = {"email": "test@example.com"}
        create_newsletter(email=data["email"], active=False)
        # post data
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(newsletters_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)

    @patch.object(GmailApi, "_send_message")
    def test_subscribe_to_newsletter_with_history_active(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        data = {"email": "test@example.com"}
        create_newsletter(email=data["email"], active=True)
        # post data
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(newsletters_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 0)


class NewsletterUnsubscribeTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/newsletter-unsubscribe"

        self.newsletter = create_newsletter(email="test@example.com")

    def test_unsubscribe_from_newsletter(self):
        # post data
        response = self.client.put(f"{self.endpoint}/{self.newsletter.uuid}", {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(get_newsletter(self.newsletter.uuid).active)

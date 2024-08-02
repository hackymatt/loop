from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from unittest.mock import patch
from .helpers import mock_send_message
import json
from utils.google.gmail import GmailApi


class ContactTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/contact"
        self.client = APIClient()

    @patch.object(GmailApi, "_send_message")
    def test_contact(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # post data
        data = {
            "full_name": "Some user name",
            "email": "some.user@example.com",
            "subject": "New contact",
            "message": "New message",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)
        self.assertEqual(_send_message_mock.call_count, 1)

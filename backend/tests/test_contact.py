from rest_framework import status
from rest_framework.test import APITestCase
from .helpers import (
    emails_sent_number,
    get_mail,
)
from django.conf import settings
import json


class ContactTest(APITestCase):
    def setUp(self):
        self.endpoint = "/contact"

    def test_contact(self):
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
        self.assertEqual(emails_sent_number(), 1)
        email = get_mail(0)
        self.assertEqual(email.to, [settings.EMAIL_FROM])
        self.assertEqual(email.subject, "Nowa wiadomość ze strony.")

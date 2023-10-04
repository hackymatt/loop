from django.test import TestCase
from rest_framework import status
from .factory import create_user, create_profile
from .helpers import login, emails_sent_number, get_mail
from django.contrib import auth


class PasswordResetTest(TestCase):
    def setUp(self):
        self.endpoint = "/password-reset"
        self.data = {"email": "email@example.com", "password": "test_password"}
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.profile = create_profile(user=self.user)

    def test_incorrect_email(self):
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
        self.assertEqual(emails_sent_number(), 0)

    def test_password_reset_success(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # password reset request
        data = {"email": self.data["email"]}
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        login(self, self.data["email"], self.data["password"])
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        self.assertEqual(emails_sent_number(), 1)
        email = get_mail(0)
        self.assertEqual(email.to, [self.data["email"]])
        self.assertEqual(email.subject, "Twoje tymczasowe hasło.")

from django.test import TestCase
from rest_framework import status
from .factory import create_user
from .helpers import (
    users_number,
    is_user_found,
    get_user,
    profiles_number,
    is_profile_found,
    get_profile,
    is_data_match,
    emails_sent_number,
    get_mail,
)


class RegisterTest(TestCase):
    def setUp(self):
        self.endpoint = "/register"
        self.data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test_email@example.com",
            "password": "TestPassword123",
            "password2": "TestPassword123",
        }
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="email@example.com",
            password="password",
            is_active=True,
        )

    def test_incorrect_email(self):
        data = self.data.copy()
        data["email"] = "email@example.com"
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 2)
        self.assertEqual(emails_sent_number(), 0)

    def test_password_strength(self):
        # new password with less than 8 characters
        new_password = "abcd"
        data = self.data.copy()
        data["password"] = new_password
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 2)
        self.assertEqual(emails_sent_number(), 0)

        # new password without numbers and uppercase letter
        new_password = "abcdefghi"
        data = self.data.copy()
        data["password"] = new_password
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(),2)
        self.assertEqual(emails_sent_number(), 0)

        # new password without uppercase letter
        new_password = "abcde1234"
        data = self.data.copy()
        data["password"] = new_password
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 2)
        self.assertEqual(emails_sent_number(), 0)

    def test_new_password_match(self):
        # new password and password 2 does not match
        new_password_2 = "TestPassword1234"
        data = self.data.copy()
        data["password2"] = new_password_2
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_number(), 2)
        self.assertEqual(emails_sent_number(), 0)

    def test_register_success(self):
        response = self.client.post(self.endpoint, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(users_number(), 3)
        self.assertEqual(profiles_number(), 1)
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
        self.assertEqual(emails_sent_number(), 1)
        email = get_mail(0)
        self.assertEqual(email.to, [self.data["email"]])
        self.assertEqual(email.subject, "Aktywuj swoje konto.")

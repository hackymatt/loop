from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_student_profile,
    create_lecturer_profile,
)
from .helpers import login, is_data_match, get_user, get_profile, get_lecturer_profile
from django.contrib import auth
import json
from base64 import b64encode


class ProfileDataTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/profile-data"
        self.data = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "test_email@example.com",
            "password": "password",
        }
        self.user = create_user(
            first_name=self.data["first_name"],
            last_name=self.data["last_name"],
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.profile = create_student_profile(profile=create_profile(user=self.user))

        self.data_lecturer = {
            "first_name": "test_first_name_lecturer",
            "last_name": "test_last_name_lecturer",
            "email": "test_email_lecturer@example.com",
            "password": "password_lecturer",
        }
        self.user_lecturer = create_user(
            first_name=self.data_lecturer["first_name"],
            last_name=self.data_lecturer["last_name"],
            email=self.data_lecturer["email"],
            password=self.data_lecturer["password"],
            is_active=True,
        )
        self.profile_lecturer = create_lecturer_profile(
            profile=create_profile(user=self.user_lecturer, user_type="W")
        )

    def test_get_profile_data_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_profile_data_lecturer(self):
        # login
        login(self, self.data_lecturer["email"], self.data_lecturer["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(response.content)
        self.assertFalse("user_type" in results.keys())

    def test_get_profile_data_other(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_profile_data_authenticated(self):
        # login
        login(self, self.data_lecturer["email"], self.data_lecturer["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(response.content)
        self.assertTrue(
            is_data_match(
                get_lecturer_profile(
                    get_profile(get_user(self.data_lecturer["email"]))
                ),
                results,
            )
        )

    def test_amend_profile_data_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "title": "new_title",
            "description": "new_description",
            "linkedin_url": "url",
        }
        response = self.client.put(self.endpoint, new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_amend_profile_data_lecturer_authenticated(self):
        # login
        login(self, self.data_lecturer["email"], self.data_lecturer["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "title": "new_title",
            "description": "new_description",
            "linkedin_url": "https://www.linkedin.com/in/abc/",
        }
        response = self.client.put(self.endpoint, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(response.content)
        self.assertTrue(
            is_data_match(
                get_lecturer_profile(
                    get_profile(get_user(self.data_lecturer["email"]))
                ),
                results,
            )
        )

    def test_amend_profile_data_other_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "title": "new_title",
            "description": "new_description",
            "linkedin_url": "url",
        }
        response = self.client.put(self.endpoint, new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

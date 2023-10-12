from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .factory import create_user, create_profile, create_image
from .helpers import login, is_data_match, filter_dict, get_user, get_profile
from django.contrib import auth
from django.core.files.uploadedfile import SimpleUploadedFile
import json


class DetailsTest(APITestCase):
    def setUp(self):
        self.endpoint = "/details"
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
        self.profile = create_profile(user=self.user)

        self.user_columns = ["first_name", "last_name", "email"]
        self.profile_columns = [
            "phone_number",
            "dob",
            "gender",
            "street_address",
            "zip_code",
            "city",
            "country",
        ]

    def test_get_details_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_details_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        user_data = filter_dict(data, self.user_columns)
        profile_data = filter_dict(data, self.profile_columns)
        self.assertTrue(is_data_match(get_user(self.data["email"]), user_data))
        self.assertTrue(
            is_data_match(get_profile(get_user(self.data["email"])), profile_data)
        )
        self.assertFalse(get_profile(get_user(self.data["email"])).image)

    def test_amend_details_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": "test_email@example.com",
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": None,
        }
        response = self.client.put(self.endpoint, new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_amend_details_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        self.profile.phone_number = "123456789"
        self.profile.dob = "2023-01-01"
        self.profile.save()

        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": "test_email@example.com",
            "phone_number": "999888777",
            "dob": None,
            "gender": "M",
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": None,
        }
        response = self.client.put(self.endpoint, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_data = filter_dict(new_data, self.user_columns)
        profile_data = filter_dict(new_data, self.profile_columns)
        self.assertTrue(is_data_match(get_user(self.data["email"]), user_data))
        self.assertTrue(
            is_data_match(get_profile(get_user(self.data["email"])), profile_data)
        )
        self.assertFalse(get_profile(get_user(self.data["email"])).image)

    def test_email_change(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "email": "new_email@example.com",
        }
        response = self.client.put(self.endpoint, new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(is_data_match(get_user(self.data["email"]), new_data))

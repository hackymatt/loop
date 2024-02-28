from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
)
from .helpers import login, filter_dict, get_profile, get_user, is_data_match
from django.contrib import auth
import json


class UsersTest(APITestCase):
    def setUp(self):
        self.endpoint = "/users"
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
        self.admin_profile = create_profile(user=self.admin_user, user_type="A")
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
        self.student_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="student_1@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.student_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="student_2@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.student_profile_1 = create_profile(user=self.student_user_1)
        self.student_profile_2 = create_profile(user=self.student_user_2)
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )

        self.user_columns = ["first_name", "last_name", "email"]
        self.profile_columns = [
            "phone_number",
            "dob",
            "gender",
            "street_address",
            "zip_code",
            "city",
            "country",
            "user_title",
        ]

    def test_get_users_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_not_admin(self):
        # no login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        results = data["results"]
        self.assertEqual(count, 6)
        for data in results:
            user_data = filter_dict(data, self.user_columns)
            profile_data = filter_dict(data, self.profile_columns)
            gender = profile_data.pop("gender")
            self.assertEqual(
                get_profile(get_user(user_data["email"])).gender,
                gender[0] if gender else None,
            )
            self.assertTrue(is_data_match(get_user(user_data["email"]), user_data))
            self.assertTrue(
                is_data_match(get_profile(get_user(user_data["email"])), profile_data)
            )
            self.assertEqual(
                get_profile(get_user(user_data["email"])).user_type,
                data["user_type"][0],
            )
            self.assertFalse(get_profile(get_user(user_data["email"])).image)

    def test_get_user_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.student_profile_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_not_admin(self):
        # no login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.student_profile_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.student_profile_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(response.content)
        user_data = filter_dict(results, self.user_columns)
        profile_data = filter_dict(results, self.profile_columns)
        gender = profile_data.pop("gender")
        self.assertEqual(get_profile(get_user(user_data["email"])).gender, gender[0])
        self.assertTrue(is_data_match(get_user(user_data["email"]), user_data))
        self.assertTrue(
            is_data_match(get_profile(get_user(user_data["email"])), profile_data)
        )
        self.assertEqual(
            get_profile(get_user(user_data["email"])).user_type, results["user_type"][0]
        )
        self.assertFalse(get_profile(get_user(user_data["email"])).image)

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
        response = self.client.put(
            f"{self.endpoint}/{self.student_profile_1.id}", new_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_amend_details_not_admin(self):
        # no login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
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
        response = self.client.put(
            f"{self.endpoint}/{self.student_profile_1.id}", new_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_amend_details_authenticated(self):
        # no login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": "student_1@example.com",
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "user_type": "W",
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": "",
        }
        response = self.client.put(
            f"{self.endpoint}/{self.student_profile_1.id}", new_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(response.content)
        user_data = filter_dict(results, self.user_columns)
        profile_data = filter_dict(results, self.profile_columns)
        gender = profile_data.pop("gender")
        self.assertEqual(get_profile(get_user(user_data["email"])).gender, gender[0])
        self.assertTrue(is_data_match(get_user(user_data["email"]), user_data))
        self.assertTrue(
            is_data_match(get_profile(get_user(user_data["email"])), profile_data)
        )
        self.assertEqual(
            get_profile(get_user(user_data["email"])).user_type, results["user_type"][0]
        )
        self.assertFalse(get_profile(get_user(user_data["email"])).image)

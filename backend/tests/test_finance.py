from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_finance,
)
from .helpers import login, is_data_match
from django.contrib import auth
import json


class FinanceTest(APITestCase):
    def setUp(self):
        self.endpoint = "/finance-details"
        self.data = {
            "email": "test_email@example.com",
            "password": "TestPassword123",
        }
        self.lecturer_data = {
            "email": "lecturer_1@example.com",
            "password": "TestPassword123",
        }
        self.student_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.lecturer_data["email"],
            password=self.lecturer_data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.student_profile = create_profile(user=self.student_user)
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )

        self.finance_1 = create_finance(
            lecturer=self.lecturer_profile_1,
            rate=150.00,
            commission=1,
        )

        self.finance_2 = create_finance(
            lecturer=self.lecturer_profile_2,
            account="48109024021679815769434176",
            rate=100,
            commission=5,
        )

        self.update_data = {
            "account": "28109024022757215857957768",
            "commission": 10,
            "rate": 110,
        }

    def test_get_finance_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_finance_not_lecturer(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_finance_authenticated(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        data["rate"] = float(data["rate"])
        self.assertTrue(is_data_match(self.finance_1, data))

    def test_update_finance_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.put(self.endpoint, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_finance_not_lecturer(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.put(self.endpoint, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lecturers_authenticated_change(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.put(self.endpoint, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["account"], self.update_data["account"])
        self.assertNotEqual(data["rate"], self.update_data["rate"])
        self.assertNotEqual(data["commission"], self.update_data["commission"])

    def test_update_lecturers_authenticated_no_change(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        self.update_data["account"] = None
        response = self.client.put(self.endpoint, self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["account"], self.update_data["account"])
        self.assertNotEqual(data["rate"], self.update_data["rate"])
        self.assertNotEqual(data["commission"], self.update_data["commission"])

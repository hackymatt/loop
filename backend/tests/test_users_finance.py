from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_admin_profile,
    create_student_profile,
    create_lecturer_profile,
    create_other_profile,
    create_finance,
)
from .helpers import (
    login,
    filter_dict,
    get_profile,
    get_user,
    is_data_match,
)
from django.contrib import auth
import json
from const import UserType


class UsersFinanceTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/users-finance"
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
            profile=create_profile(user=self.admin_user, user_type=UserType.ADMIN)
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
        self.lecturer_data = {
            "email": "lecturer_1@example.com",
            "password": "TestPassword123",
        }
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
        self.other_data = {
            "email": "other_1@example.com",
            "password": "TestPassword123",
        }
        self.other_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.other_data["email"],
            password=self.other_data["password"],
            is_active=False,
        )
        self.student_profile_1 = create_student_profile(
            profile=create_profile(user=self.student_user_1)
        )
        self.student_profile_2 = create_student_profile(
            profile=create_profile(user=self.student_user_2)
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(
                user=self.lecturer_user_1,
                user_type=UserType.INSTRUCTOR,
            )
        )
        create_finance(
            lecturer=self.lecturer_profile_1, account="", rate=125, commission=4
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(
                user=self.lecturer_user_2, user_type=UserType.INSTRUCTOR
            )
        )
        self.other_profile = create_other_profile(
            profile=create_profile(user=self.other_user_1, user_type=UserType.OTHER)
        )

    def test_get_users_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_not_admin(self):
        # login
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
        self.assertEqual(count, 2)
        for data in results:
            self.assertEqual(data, {'account': '', 'commission': 4, 'rate': 125.0})

    def test_get_user_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.student_profile_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_not_admin(self):
        # login
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
        response = self.client.get(
            f"{self.endpoint}/{self.lecturer_profile_1.profile.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(response.content)
        self.assertEqual(results, {'rate': 125.0, 'commission': 4, 'account': ''})

    def test_amend_details_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "rate": 125,
            "commission": 4,
            "account": "48109024021679815769434176"
        }
        response = self.client.put(
            f"{self.endpoint}/{self.student_profile_1.id}", new_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_amend_details_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "rate": 125,
            "commission": 4,
            "account": "48109024021679815769434176"
        }
        response = self.client.put(
            f"{self.endpoint}/{self.student_profile_1.id}", new_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_amend_financial_details_authenticated_no_change(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "rate": 125,
            "commission": 4,
            "account": "48109024021679815769434176"
        }
        response = self.client.put(
            f"{self.endpoint}/{self.lecturer_profile_1.profile.id}", new_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(response.content)
        self.assertEqual(results, new_data)



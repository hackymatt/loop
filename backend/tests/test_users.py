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
    is_admin_profile_found,
    is_lecturer_profile_found,
    is_student_profile_found,
    is_other_profile_found,
    is_float,
)
from django.contrib import auth
import json


class UsersTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/users"
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
                user_type="W",
            )
        )
        create_finance(
            lecturer=self.lecturer_profile_1, account="", rate=125, commission=4
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )
        self.other_profile = create_other_profile(
            profile=create_profile(user=self.other_user_1, user_type="I")
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
        ]

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
        self.assertEqual(count, 9)
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
            f"{self.endpoint}/{self.student_profile_1.profile.id}"
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

    def test_create_user_unauthenticated(self):
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
            "user_type": "I",
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": None,
        }
        response = self.client.post(self.endpoint, new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_not_admin(self):
        # login
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
            "user_type": "I",
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": None,
        }
        response = self.client.post(self.endpoint, new_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_incorrect_user_type(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": "lecturer_1@example.com",
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "user_type": "A",
            "rate": 100,
            "commission": 1,
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": "",
        }
        response = self.client.post(self.endpoint, new_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": "abc@example.com",
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "user_type": "I",
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": "",
        }
        response = self.client.post(self.endpoint, new_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
        self.assertTrue(
            is_other_profile_found(get_profile(get_user(user_data["email"])))
        )

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
        # login
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

    def test_amend_details_authenticated_student_to_lecturer(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": self.data["email"],
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "user_type": "W",
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": "",
            "rate": 100,
            "commission": 10,
        }
        response = self.client.put(
            f"{self.endpoint}/{self.student_profile_1.profile.id}", new_data
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
        self.assertFalse(
            is_student_profile_found(get_profile(get_user(user_data["email"])))
        )
        self.assertTrue(
            is_lecturer_profile_found(get_profile(get_user(user_data["email"])))
        )

    def test_amend_details_authenticated_student_to_other(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": self.other_data["email"],
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "user_type": "I",
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": "",
        }
        response = self.client.put(
            f"{self.endpoint}/{self.student_profile_1.profile.id}", new_data
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
        self.assertFalse(
            is_student_profile_found(get_profile(get_user(user_data["email"])))
        )
        self.assertTrue(
            is_other_profile_found(get_profile(get_user(user_data["email"])))
        )

    def test_amend_details_authenticated_lecturer_to_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": self.lecturer_data["email"],
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "user_type": "A",
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": "",
        }
        response = self.client.put(
            f"{self.endpoint}/{self.lecturer_profile_1.profile.id}", new_data
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
        self.assertFalse(
            is_lecturer_profile_found(get_profile(get_user(user_data["email"])))
        )
        self.assertTrue(
            is_admin_profile_found(get_profile(get_user(user_data["email"])))
        )

    def test_amend_details_authenticated_admin_to_student(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": self.admin_data["email"],
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "user_type": "S",
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": "",
        }
        response = self.client.put(
            f"{self.endpoint}/{self.admin_profile.profile.id}", new_data
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
        self.assertFalse(
            is_admin_profile_found(get_profile(get_user(user_data["email"])))
        )
        self.assertTrue(
            is_student_profile_found(get_profile(get_user(user_data["email"])))
        )

    def test_amend_details_authenticated_other_to_student(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": self.other_data["email"],
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "user_type": "S",
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": "",
        }
        response = self.client.put(
            f"{self.endpoint}/{self.other_profile.profile.id}", new_data
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
        self.assertFalse(
            is_admin_profile_found(get_profile(get_user(user_data["email"])))
        )
        self.assertTrue(
            is_student_profile_found(get_profile(get_user(user_data["email"])))
        )

    def test_change_user_type(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": "lecturer_1@example.com",
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "user_type": "T",
            "rate": 100,
            "commission": 1,
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": "",
        }
        response = self.client.put(
            f"{self.endpoint}/{self.lecturer_profile_1.profile.id}", new_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_amend_financial_details_authenticated_change(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": "lecturer_1@example.com",
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "user_type": "W",
            "rate": 100,
            "commission": 1,
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": "",
        }
        response = self.client.put(
            f"{self.endpoint}/{self.lecturer_profile_1.profile.id}", new_data
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

    def test_amend_financial_details_authenticated_no_change(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # new data
        new_data = {
            "first_name": "Name",
            "last_name": "LastName",
            "email": "lecturer_1@example.com",
            "phone_number": "999888777",
            "dob": "1900-01-01",
            "gender": "M",
            "user_type": "W",
            "rate": 125,
            "commission": 4,
            "street_address": "abc",
            "zip_code": "30-100",
            "city": "Miasto",
            "country": "Polska",
            "image": "",
        }
        response = self.client.put(
            f"{self.endpoint}/{self.lecturer_profile_1.profile.id}", new_data
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


class UsersFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/users"
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
        self.student_profile_1 = create_student_profile(
            profile=create_profile(user=self.student_user_1)
        )
        self.student_profile_2 = create_student_profile(
            profile=create_profile(user=self.student_user_2)
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W"),
            title="soft",
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

    def test_first_name_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "first_name"
        variable = "first"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_last_name_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "last_name"
        variable = "last"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_email_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "email"
        variable = "student_2"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_active_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "active"
        variable = "true"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 8)
        values = list(set([True == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_gender_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "gender"
        variable = "m"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_user_type_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "user_type"
        variable = "W"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        values = list(set([variable == record[column][0] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_created_at_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "created_at"
        variable = str(self.admin_profile.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 8)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_phone_number_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "phone_number"
        variable = "123"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_dob_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "dob"
        variable = "1999"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_street_address_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "street_address"
        variable = "tree"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_zip_code_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "zip_code"
        variable = "zip"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_city_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "city"
        variable = "ty"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_country_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "country"
        variable = "try"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class UsersOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/users"
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
        self.student_profile_1 = create_student_profile(
            profile=create_profile(user=self.student_user_1)
        )
        self.student_profile_2 = create_student_profile(
            profile=create_profile(user=self.student_user_2)
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W")
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

        self.fields = [
            "first_name",
            "last_name",
            "email",
            "active",
            "gender",
            "user_type",
            "created_at",
            "phone_number",
            "dob",
            "street_address",
            "zip_code",
            "city",
            "country",
        ]

    def test_ordering(self):
        for field in self.fields:
            login(self, self.admin_data["email"], self.admin_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 8)
            field_values = [user[field] for user in results]
            field_values = [value for value in field_values if value is not None]
            if isinstance(field_values[0], dict):
                self.assertEqual(
                    field_values, sorted(field_values, key=lambda d: d["name"])
                )
            else:
                field_values = [
                    field_value if not is_float(field_value) else float(field_value)
                    for field_value in field_values
                ]
                self.assertEqual(field_values, sorted(field_values))
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by=-{field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 8)
            field_values = [user[field] for user in results]
            field_values = [value for value in field_values if value is not None]
            if isinstance(field_values[0], dict):
                self.assertEqual(
                    field_values,
                    sorted(field_values, key=lambda d: d["name"], reverse=True),
                )
            else:
                field_values = [
                    field_value if not is_float(field_value) else float(field_value)
                    for field_value in field_values
                ]
                self.assertEqual(field_values, sorted(field_values, reverse=True))

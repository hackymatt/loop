from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_technology,
    create_technology_obj,
)
from .helpers import (
    login,
    technologies_number,
)
from django.contrib import auth
import json


class TechnologyTest(APITestCase):
    def setUp(self):
        self.endpoint = "/technologies"
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
        self.profile = create_profile(user=self.user)

        create_technology(name="Python")
        self.technology = create_technology(name="JavaScript")
        create_technology(name="C++")
        create_technology(name="C#")
        create_technology(name="VBA")

        self.new_technology = create_technology_obj(name="Git")

        self.amend_technology = create_technology_obj(name="JS")

    def test_get_technologies_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(technologies_number(), count)

    def test_get_technologies_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(technologies_number(), count)

    def test_create_technologies_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_technology
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(technologies_number(), 5)

    def test_create_technologies_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_technology
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(technologies_number(), 5)

    def test_create_technologies_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_technology
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(data["name"], self.new_technology["name"])
        self.assertEqual(technologies_number(), 6)

    def test_update_technologies_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_technology
        response = self.client.put(f"{self.endpoint}/{self.technology.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(technologies_number(), 5)

    def test_update_technologies_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_technology
        response = self.client.put(f"{self.endpoint}/{self.technology.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_technologies_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_technology
        response = self.client.put(f"{self.endpoint}/{self.technology.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["name"], self.amend_technology["name"])

    def test_delete_technologies_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.technology.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(technologies_number(), 5)

    def test_delete_technologies_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.technology.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(technologies_number(), 5)

    def test_delete_technologies_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.technology.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(technologies_number(), 4)

from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_technology,
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
        create_technology(name="Python")
        create_technology(name="JavaScript")
        create_technology(name="C++")
        create_technology(name="C#")
        create_technology(name="VBA")

    def test_get_technologies_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(technologies_number(), len(data))

    def test_get_technologies_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(technologies_number(), len(data))

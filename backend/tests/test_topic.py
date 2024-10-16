from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_admin_profile,
    create_student_profile,
    create_topic,
    create_topic_obj,
)
from .helpers import (
    login,
    topics_number,
)
from django.contrib import auth
import json


class TopicTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/topics"
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
        self.profile = create_student_profile(profile=create_profile(user=self.user))

        create_topic(name="A")
        self.topic = create_topic(name="B")
        create_topic(name="C")
        create_topic(name="D")
        create_topic(name="E")

        self.new_topic = create_topic_obj(name="F")

        self.amend_topic = create_topic_obj(name=self.topic.name)

    def test_get_topics_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(topics_number(), count)

    def test_get_topics_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(topics_number(), count)

    def test_create_topics_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_topic
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(topics_number(), 5)

    def test_create_topics_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_topic
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(topics_number(), 5)

    def test_create_topics_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.new_topic
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(data["name"], self.new_topic["name"])
        self.assertEqual(topics_number(), 6)

    def test_update_topics_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_topic
        response = self.client.put(f"{self.endpoint}/{self.topic.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(topics_number(), 5)

    def test_update_topics_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_topic
        response = self.client.put(f"{self.endpoint}/{self.topic.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_topics_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = self.amend_topic
        response = self.client.put(f"{self.endpoint}/{self.topic.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["name"], self.amend_topic["name"])

    def test_delete_topics_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.topic.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(topics_number(), 5)

    def test_delete_topics_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.topic.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(topics_number(), 5)

    def test_delete_topics_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.topic.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(topics_number(), 4)


class TopicFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/topics"
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
        self.topic = create_topic(name="A")
        create_topic(name="B")
        create_topic(name="C")
        create_topic(name="D")
        create_topic(name="E")

    def test_name_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?name=A")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        prices = [record["name"] for record in results]
        self.assertEqual(prices, ["A"])

    def test_created_at_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        date = str(self.topic.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?created_at={date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        dates = list(set([date in record["created_at"] for record in results]))
        self.assertTrue(len(dates) == 1)
        self.assertTrue(dates[0])


class TopicOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/topics"
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
        create_topic(name="A")
        create_topic(name="B")
        create_topic(name="C")
        create_topic(name="D")
        create_topic(name="E")

        self.fields = ["name", "created_at"]

    def is_float(self, element: any) -> bool:
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def test_ordering(self):
        for field in self.fields:
            self.assertFalse(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 5)
            field_values = [course[field] for course in results]
            if isinstance(field_values[0], dict):
                self.assertEqual(
                    field_values, sorted(field_values, key=lambda d: d["name"])
                )
            else:
                field_values = [
                    field_value
                    if not self.is_float(field_value)
                    else float(field_value)
                    for field_value in field_values
                ]
                self.assertEqual(field_values, sorted(field_values))
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by=-{field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 5)
            field_values = [course[field] for course in results]
            if isinstance(field_values[0], dict):
                self.assertEqual(
                    field_values,
                    sorted(field_values, key=lambda d: d["name"], reverse=True),
                )
            else:
                field_values = [
                    field_value
                    if not self.is_float(field_value)
                    else float(field_value)
                    for field_value in field_values
                ]
                self.assertEqual(field_values, sorted(field_values, reverse=True))

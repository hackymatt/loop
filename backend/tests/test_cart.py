from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_lesson,
    create_technology_obj,
    create_cart,
)
from .helpers import login, cart_number
from django.contrib import auth
import json


class CartTest(APITestCase):
    def setUp(self):
        self.endpoint = "/cart"
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

        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/hackymatt/course/lesson",
            price="9.99",
            technologies=[create_technology_obj(name="Python")],
        )
        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/hackymatt/course/lesson",
            price="2.99",
            technologies=[create_technology_obj(name="Python")],
        )

        self.lesson_3 = create_lesson(
            title="JS lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/hackymatt/course/lesson",
            price="9.99",
            technologies=[create_technology_obj(name="JS")],
        )
        self.lesson_4 = create_lesson(
            title="JS lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/hackymatt/course/lesson",
            price="2.99",
            technologies=[create_technology_obj(name="JS")],
        )
        self.lesson_5 = create_lesson(
            title="JS lesson 3",
            description="bbbb",
            duration="120",
            github_url="https://github.com/hackymatt/course/lesson",
            price="2.99",
            technologies=[create_technology_obj(name="JS")],
        )

        self.lesson_6 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/hackymatt/course/lesson",
            price="9.99",
            technologies=[create_technology_obj(name="VBA")],
        )

        self.lessons = [
            self.lesson_1,
            self.lesson_2,
            self.lesson_3,
            self.lesson_4,
            self.lesson_5,
            self.lesson_5,
        ]

        self.cart = []
        for lesson in self.lessons:
            self.cart.append(
                create_cart(
                    student=self.profile,
                    lesson=lesson,
                )
            )

        self.new_items = [self.lesson_6]
        self.delete_item = self.cart[0]

    def test_get_cart_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_cart_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 6)

    def test_add_to_cart_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        data = {
            "lessons": [new_item.id for new_item in self.new_items],
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_to_cart_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = {
            "lessons": [new_item.id for new_item in self.new_items],
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(cart_number(), 7)

    def test_delete_from_cart_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.delete_item.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_from_cart_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.delete_item.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(cart_number(), 5)

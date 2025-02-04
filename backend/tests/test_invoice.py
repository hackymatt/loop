from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from unittest.mock import patch
from .factory import (
    create_user,
    create_profile,
    create_student_profile,
    create_admin_profile,
    create_lesson,
    create_technology,
    create_purchase,
    create_payment,
)
from .helpers import (
    login,
    mock_send_message,
)
import json
from django.contrib import auth
from utils.google.gmail import GmailApi


class InvoiceTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/invoice"
        self.client = APIClient()

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
            "email": "user@example.com",
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

        self.technology = create_technology(name="Python")

        # course 1
        self.lesson = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology],
        )

        self.payment_1 = create_payment(amount=10000, status="P")
        self.payment_2 = create_payment(amount=10000, status="P")

        purchase = create_purchase(
            lesson=self.lesson,
            student=self.profile,
            price=self.lesson.price,
            payment=self.payment_1,
        )

        self.invoice_1 = {
            "customer": {
                "id": purchase.student.id,
                "full_name": f"{purchase.student.profile.user.first_name} {purchase.student.profile.user.last_name}",
                "street_address": purchase.student.profile.street_address,
                "city": purchase.student.profile.city,
                "zip_code": purchase.student.profile.zip_code,
                "country": purchase.student.profile.country,
            },
            "items": [
                {
                    "id": purchase.lesson.id,
                    "name": purchase.lesson.title,
                    "price": purchase.lesson.price,
                }
            ],
            "payment": {
                "id": self.payment_1.id,
                "amount": self.payment_1.amount / 100,
                "status": "Zapłacono" if self.payment_1.status == "S" else "Do zapłaty",
                "method": "Przelewy24",
                "account": "",
            },
            "notes": "",
        }
        self.invoice_2 = {
            "customer": {
                "id": 2,
                "full_name": "Jan Kowalski",
                "street_address": "Ulica Nazwa 1",
                "city": "Miasto",
                "zip_code": "12-345",
                "country": "Polska",
            },
            "items": [
                {
                    "id": 1,
                    "name": "Produkt 1",
                    "price": 29.99,
                },
                {
                    "id": 2,
                    "name": "Produkt 2",
                    "price": 329.99,
                },
                {
                    "id": 3,
                    "name": "Produkt 3",
                    "price": 19.99,
                },
            ],
            "payment": {
                "id": self.payment_2.id,
                "amount": self.payment_2.amount / 100,
                "status": "Zapłacono" if self.payment_2.status == "S" else "Do zapłaty",
                "method": "Przelew",
                "account": "123456",
            },
            "notes": "Notatka",
        }

    def test_get_invoice_unauthorized(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.payment_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invoice_authorized(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.payment_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_invoice_authorized_admin_1(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.payment_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertDictEqual(data, self.invoice_1)

    def test_get_invoice_authorized_admin_2(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.payment_2.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertDictEqual(
            data,
            {
                "customer": {
                    "id": "",
                    "full_name": "",
                    "street_address": "",
                    "city": "",
                    "zip_code": "",
                    "country": "",
                },
                "items": [],
                "payment": {
                    "id": self.payment_2.id,
                    "amount": self.payment_2.amount / 100,
                    "status": "Do zapłaty",
                    "method": "Przelew",
                    "account": "PL 59 1160 2202 0000 0006 2440 0188",
                },
                "notes": "",
            },
        )

    def test_create_invoice_unauthorized(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post
        data = self.invoice_1
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invoice_authorized(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post
        data = self.invoice_1
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(GmailApi, "_send_message")
    def test_create_invoice_authorized_admin(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post
        data = self.invoice_1
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(_send_message_mock.call_count, 1)

    @patch.object(GmailApi, "_send_message")
    def test_create_invoice_authorized_admin(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post
        data = self.invoice_2
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(_send_message_mock.call_count, 1)

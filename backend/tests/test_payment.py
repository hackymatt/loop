from rest_framework import status
from rest_framework.test import APIClient, APITestCase
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
    create_payment_obj,
)
from .helpers import (
    login,
    mock_verify_payment,
    mock_send_message,
    notifications_number,
    payments_number,
    is_data_match,
    is_float,
)
import json
from django.contrib import auth
from utils.przelewy24.payment import Przelewy24Api
from utils.google.gmail import GmailApi
from const import UserType


class PaymentVerifyTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/payment-verify"
        self.client = APIClient()

        self.payment = create_payment(amount=10000, status="P")

    @patch.object(Przelewy24Api, "verify")
    def test_verify_no_matching_record(self, verify_mock):
        mock_verify_payment(mock=verify_mock, result=True)
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "sessionId": str(self.payment.session_id),
            "orderId": 12345,
            "amount": int(self.payment.amount) * 2,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(Przelewy24Api, "verify")
    def test_verify_failure(self, verify_mock):
        mock_verify_payment(mock=verify_mock, result=False)
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "sessionId": str(self.payment.session_id),
            "orderId": 12345,
            "amount": int(self.payment.amount),
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(Przelewy24Api, "verify")
    def test_verify_success(self, verify_mock):
        mock_verify_payment(mock=verify_mock, result=True)
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "sessionId": str(self.payment.session_id),
            "orderId": 12345,
            "amount": int(self.payment.amount),
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PaymentStatusTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/payment-status"
        self.client = APIClient()

        self.data = {
            "email": "user@example.com",
            "password": "TestPassword123",
        }
        self.user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="user2@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.profile_1 = create_student_profile(
            profile=create_profile(user=self.user_1)
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )

        self.technology_1 = create_technology(name="Python")

        # course 1
        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_1],
        )

        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile_1,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )
        self.purchase_2 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile_2,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )

    def test_get_status_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(GmailApi, "_send_message")
    def test_get_status_incorrect(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?session_id={self.purchase_2.payment.session_id}"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(notifications_number(), 0)
        self.assertEqual(_send_message_mock.call_count, 0)

    @patch.object(GmailApi, "_send_message")
    def test_get_status_correct_success(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?session_id={self.purchase_1.payment.session_id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "amount": int(self.purchase_1.payment.amount),
                "currency": self.purchase_1.payment.currency.value,
                "method": self.purchase_1.payment.method.value,
                "notes": None,
                "order_id": self.purchase_1.payment.order_id,
                "session_id": str(self.purchase_1.payment.session_id),
                "id": self.purchase_1.payment.id,
                "status": self.purchase_1.payment.status.value,
                "created_at": str(self.purchase_1.payment.created_at).replace(" ", "T")[
                    0:26
                ]
                + "Z",
            },
        )
        self.assertEqual(notifications_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)

    @patch.object(GmailApi, "_send_message")
    def test_get_status_correct_failure(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        self.purchase_1.payment.status = "P"
        self.purchase_1.payment.save()
        response = self.client.get(
            f"{self.endpoint}?session_id={self.purchase_1.payment.session_id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        data["status"] = data["status"][0]
        self.assertEqual(
            data,
            {
                "amount": int(self.purchase_1.payment.amount),
                "currency": self.purchase_1.payment.currency.value,
                "method": self.purchase_1.payment.method.value,
                "notes": None,
                "order_id": self.purchase_1.payment.order_id,
                "session_id": str(self.purchase_1.payment.session_id),
                "id": self.purchase_1.payment.id,
                "status": "F",
                "created_at": str(self.purchase_1.payment.created_at).replace(" ", "T")[
                    0:26
                ]
                + "Z",
            },
        )
        self.assertEqual(notifications_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)


class PaymentTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/payments"
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

        self.payment_1 = create_payment(amount=100)
        self.payment_2 = create_payment(amount=50, status="P")
        self.payment_3 = create_payment(amount=555, status="P")
        self.payment_4 = create_payment(amount=22, status="F")
        self.payment_5 = create_payment(amount=44)

        self.technology = create_technology(name="Python")
        self.lesson = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology],
        )
        self.purchase = create_purchase(
            lesson=self.lesson,
            student=self.profile,
            price=self.lesson.price,
            payment=self.payment_5,
        )

        self.new_payment = create_payment_obj(
            amount=500, status="Pending", notes="test"
        )
        self.edit_payment = create_payment_obj(
            amount=self.payment_1.amount, status="Success", notes="test"
        )

    def test_get_payments_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_payments_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_payments_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        self.assertEqual(records_count, 5)

    def test_get_payment_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.payment_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_payment_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.payment_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_payment_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.payment_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        payment_status = data.pop("status")
        self.assertTrue(is_data_match(self.payment_1, data))
        self.assertEqual(payment_status, self.payment_1.status)

    def test_create_payment_not_authenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_payment
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(payments_number(), 5)

    def test_create_payment_authenticated_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_payment
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(payments_number(), 5)

    def test_create_payment_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_payment
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(payments_number(), 6)

    def test_edit_payment_not_authenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.edit_payment
        response = self.client.put(f"{self.endpoint}/{self.payment_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_payment_authenticated_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.edit_payment
        response = self.client.put(f"{self.endpoint}/{self.payment_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_payment_authenticated_admin_not_allowed(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.payment_1.amount = self.payment_1.amount * 10
        self.payment_1.save()
        self.purchase.payment = self.payment_1
        self.purchase.save()
        data = self.edit_payment
        response = self.client.put(
            f"{self.endpoint}/{self.payment_1.id}",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_edit_payment_authenticated_admin_allowed(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.payment_1.amount = self.payment_1.amount * 10
        self.payment_1.save()
        data = self.edit_payment
        response = self.client.put(
            f"{self.endpoint}/{self.payment_1.id}",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.payment_1.refresh_from_db()
        payment_status = data.pop("status")
        amount = data.pop("amount")
        self.assertTrue(is_data_match(self.payment_1, data))
        self.assertEqual(payment_status, self.payment_1.status)
        self.assertEqual(amount, self.payment_1.amount)

    def test_delete_payment_not_authenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        response = self.client.delete(f"{self.endpoint}/{self.payment_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_payment_authenticated_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        response = self.client.delete(f"{self.endpoint}/{self.payment_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_payment_authenticated_admin_not_allowed(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.purchase.payment = self.payment_1
        self.purchase.save()
        response = self.client.delete(f"{self.endpoint}/{self.payment_1.id}")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(payments_number(), 5)

    def test_delete_payment_authenticated_admin_allowed(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        response = self.client.delete(f"{self.endpoint}/{self.payment_1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(payments_number(), 4)


class PaymentFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/payments"
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

        self.payment_1 = create_payment(amount=100)
        self.payment_2 = create_payment(amount=50, status="P")
        self.payment_3 = create_payment(amount=555, status="P")
        self.payment_4 = create_payment(amount=22, status="F")
        self.payment_5 = create_payment(amount=44)

    def test_session_id_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        session_id = str(self.payment_1.session_id)
        response = self.client.get(f"{self.endpoint}?session_id={session_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        titles = list(set([session_id in record["session_id"] for record in results]))
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0])

    def test_amount_from_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        amount_from = 49
        response = self.client.get(f"{self.endpoint}?amount_from={amount_from}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        titles = list(
            set([record["amount"] >= amount_from * 100 for record in results])
        )
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0])

    def test_amount_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        amount_to = 99
        response = self.client.get(f"{self.endpoint}?amount_to={amount_to}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        titles = list(set([record["amount"] <= amount_to * 100 for record in results]))
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0])

    def test_status_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        status_var = self.payment_4.status
        response = self.client.get(f"{self.endpoint}?status={status_var}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        titles = list(set([status_var in record["status"] for record in results]))
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0])

    def test_created_at_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        date = str(self.payment_1.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?created_at={date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        dates = list(set([date in record["created_at"] for record in results]))
        self.assertTrue(len(dates) == 1)
        self.assertTrue(dates[0])


class PaymentOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/payments"
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

        self.payment_1 = create_payment(amount=100)
        self.payment_2 = create_payment(amount=50, status="P")
        self.payment_3 = create_payment(amount=555, status="P")
        self.payment_4 = create_payment(amount=22, status="F")
        self.payment_5 = create_payment(amount=44)

        self.fields = [
            "session_id",
            "amount",
            "status",
            "created_at",
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
            self.assertEqual(count, 5)
            field_values = [course[field] for course in results]
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
            self.assertEqual(count, 5)
            field_values = [course[field] for course in results]
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

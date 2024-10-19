from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from unittest.mock import patch
from .factory import (
    create_user,
    create_profile,
    create_admin_profile,
    create_student_profile,
    create_newsletter,
    create_coupon,
    create_lecturer_profile,
    create_notification,
)
from .helpers import (
    login,
    newsletters_number,
    get_newsletter,
    is_data_match,
    mock_send_message,
    is_float,
)
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from utils.google.gmail import GmailApi


class NewsletterEntriesTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/newsletter"

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

        self.active_newsletters = [
            create_newsletter(email=f"test_active_{i}@example.com") for i in range(15)
        ]
        self.inactive_newsletters = [
            create_newsletter(email=f"test_inactive_{i}@example.com", active=False)
            for i in range(5)
        ]

    def test_get_newsletter_entries_unauthenticated(self):
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_newsletter_entries_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_newsletter_entries_success(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 20)

    def test_get_newsletter_entry_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.active_newsletters[0].id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_newsletter_entry_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.active_newsletters[0].id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_newsletter_entry_success(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.active_newsletters[0].id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        newsletter = get_newsletter(uuid=self.active_newsletters[0].uuid)
        self.assertTrue(is_data_match(newsletter, data))


class NewsletterSubscribeTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/newsletter-subscribe"
        self.client = APIClient()

    @patch.object(GmailApi, "_send_message")
    def test_subscribe_to_newsletter_without_history_with_coupon(
        self, _send_message_mock
    ):
        mock_send_message(mock=_send_message_mock)
        # post data
        data = {"email": "test@example.com"}
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(newsletters_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)

    @patch.object(GmailApi, "_send_message")
    def test_subscribe_to_newsletter_without_history_without_coupon(
        self, _send_message_mock
    ):
        mock_send_message(mock=_send_message_mock)
        # post data
        data = {"email": "test@example.com"}
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(newsletters_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)

    @patch.object(GmailApi, "_send_message")
    def test_subscribe_to_newsletter_with_history_inactive(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        data = {"email": "test@example.com"}
        create_newsletter(email=data["email"], active=False)
        # post data
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(newsletters_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)

    @patch.object(GmailApi, "_send_message")
    def test_subscribe_to_newsletter_with_history_active(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        data = {"email": "test@example.com"}
        create_newsletter(email=data["email"], active=True)
        # post data
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(newsletters_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 0)


class NewsletterUnsubscribeTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/newsletter-unsubscribe"

        self.newsletter = create_newsletter(email="test@example.com")

    def test_unsubscribe_from_newsletter(self):
        # post data
        response = self.client.put(f"{self.endpoint}/{self.newsletter.uuid}", {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(get_newsletter(self.newsletter.uuid).active)


class NewsletterEntriesFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/newsletter"

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

        self.active_newsletters = [
            create_newsletter(email=f"test_active_{i}@example.com") for i in range(15)
        ]
        self.inactive_newsletters = [
            create_newsletter(email=f"test_inactive_{i}@example.com", active=False)
            for i in range(5)
        ]

    def test_id_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "uuid"
        variable = str(self.active_newsletters[0].uuid)
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_email_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "email"
        variable = "test_active"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 15)
        values = list(set([variable in record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_active_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "active"
        variable = True
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 15)
        values = list(set([variable == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_created_at_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "created_at"
        variable = str(self.active_newsletters[0].created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 20)
        values = list(set([variable in record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class NotificationFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/notifications"
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

        self.lecturer_data = {
            "email": "lecturer_1@example.com",
            "password": "TestPassword123",
        }
        self.lecturer_user = create_user(
            first_name="l1_first_name",
            last_name="l1_last_name",
            email=self.lecturer_data["email"],
            password=self.lecturer_data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
        )

        self.student_notifications = [
            create_notification(
                profile=self.profile.profile,
                title=f"title",
                subtitle=f"subtitle",
                description=f"description",
                status="READ",
                path=f"path",
                icon=f"icon",
            )
        ]
        for i in range(50):
            self.student_notifications.append(
                create_notification(
                    profile=self.profile.profile,
                    title=f"title_{i}",
                    subtitle=f"subtitle{i}",
                    description=f"description{i}",
                    status="NEW",
                    path=f"path{i}",
                    icon=f"icon{i}",
                )
            )

        self.lecturer_notifications = []
        for i in range(100):
            self.lecturer_notifications.append(
                create_notification(
                    profile=self.lecturer_profile.profile,
                    title=f"title_{i}",
                    subtitle=f"subtitle{i}",
                    description=f"description{i}",
                    status="NEW",
                    path=f"path{i}",
                    icon=f"icon{i}",
                )
            )

    def test_status_filter(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "status"
        variable = self.student_notifications[0].status
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable in record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class NewsletterEntriesOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/newsletter"

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

        self.active_newsletters = [
            create_newsletter(email=f"test_active_{i}@example.com") for i in range(15)
        ]
        self.inactive_newsletters = [
            create_newsletter(email=f"test_inactive_{i}@example.com", active=False)
            for i in range(5)
        ]

        self.fields = [
            "uuid",
            "email",
            "active",
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
            self.assertEqual(count, 20)
            if "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course[field1] for course in results if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
            elif "coupon_code" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "user_email" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            else:
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
            self.assertEqual(count, 20)
            if "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course[field1] for course in results if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
            elif "coupon_code" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "user_email" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            else:
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

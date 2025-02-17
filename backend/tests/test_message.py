from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from unittest.mock import patch
from .factory import (
    create_user,
    create_profile,
    create_student_profile,
    create_lecturer_profile,
    create_admin_profile,
    create_message,
)
from .helpers import (
    login,
    messages_number,
    notifications_number,
    mock_send_message,
    is_float,
)
from django.contrib import auth
import json
from message.utils import remove_old_messages
from datetime import timedelta
from utils.google.gmail import GmailApi
from const import UserType, StatusType


class MessageTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.endpoint = "/api/messages"
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
            profile=create_profile(
                user=self.lecturer_user, user_type=UserType.INSTRUCTOR
            )
        )

        self.student_messages = []
        for i in range(50):
            self.student_messages.append(
                create_message(
                    sender=self.lecturer_profile.profile,
                    recipient=self.profile.profile,
                    subject=f"subject{i}",
                    body=f"body{i}",
                    status=StatusType.NEW,
                )
            )

        self.lecturer_messages = []
        for i in range(100):
            self.lecturer_messages.append(
                create_message(
                    sender=self.profile.profile,
                    recipient=self.lecturer_profile.profile,
                    subject=f"subject{i}",
                    body=f"body{i}",
                    status=StatusType.NEW,
                )
            )

        self.create_data_1 = {
            "subject": "new subject",
            "body": "new body",
            "status": StatusType.NEW,
            "recipient_id": self.profile.id,
            "recipient_type": "Student",
        }

        self.create_data_2 = {
            "subject": "new subject",
            "body": "new body",
            "status": StatusType.NEW,
            "recipient_id": self.lecturer_profile.id,
            "recipient_type": "Wykładowca",
        }

        self.create_data_3 = {
            "subject": "new subject",
            "body": "new body",
            "status": StatusType.NEW,
            "recipient_id": self.admin_profile.id,
            "recipient_type": "Admin",
        }

        self.create_data_4 = {
            "subject": "new subject",
            "body": "new body",
            "status": StatusType.NEW,
            "recipient_uuid": self.lecturer_profile.profile.uuid,
        }

        self.edit_data = {
            "subject": self.student_messages[0].subject,
            "body": self.student_messages[0].body,
            "status": StatusType.READ,
        }

    def test_get_messages_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_messages_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 150)

    def test_get_message_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_message_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.student_messages[0].id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_message_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.post(self.endpoint, data=self.create_data_1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(GmailApi, "_send_message")
    def test_create_message_authenticated_1(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.post(self.endpoint, data=self.create_data_1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(data["status"], self.create_data_1["status"])
        self.assertEqual(data["recipient_id"], self.profile.profile.id)
        self.assertEqual(notifications_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)

    @patch.object(GmailApi, "_send_message")
    def test_create_message_authenticated_2(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.post(self.endpoint, data=self.create_data_2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(data["status"], self.create_data_2["status"])
        self.assertEqual(data["recipient_id"], self.lecturer_profile.profile.id)
        self.assertEqual(notifications_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)

    @patch.object(GmailApi, "_send_message")
    def test_create_message_authenticated_3(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.post(self.endpoint, data=self.create_data_3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(data["status"], self.create_data_3["status"])
        self.assertEqual(data["recipient_id"], self.admin_profile.profile.id)
        self.assertEqual(notifications_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)

    @patch.object(GmailApi, "_send_message")
    def test_create_message_authenticated_4(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.post(self.endpoint, data=self.create_data_4)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(data["status"], self.create_data_4["status"])
        self.assertEqual(data["recipient_id"], self.lecturer_profile.profile.id)
        self.assertEqual(notifications_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)

    def test_edit_message_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.put(
            f"{self.endpoint}/{self.student_messages[0].id}", data=self.edit_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_message_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.put(
            f"{self.endpoint}/{self.student_messages[0].id}", data=self.edit_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["status"], self.edit_data["status"])


class MessageUtilsTest(APITestCase):
    def setUp(self):
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
            profile=create_profile(
                user=self.lecturer_user, user_type=UserType.INSTRUCTOR
            )
        )

        self.messages = []
        for i in range(50):
            self.messages.append(
                create_message(
                    sender=self.lecturer_profile.profile,
                    recipient=self.profile.profile,
                    subject=f"subject{i}",
                    body=f"body{i}",
                    status=StatusType.READ,
                )
            )

        for i in range(100):
            self.messages.append(
                create_message(
                    sender=self.profile.profile,
                    recipient=self.lecturer_profile.profile,
                    subject=f"subject{i}",
                    body=f"body{i}",
                    status=StatusType.READ,
                )
            )

        for index, message in enumerate(self.messages):
            message.created_at = message.created_at - timedelta(days=index)
            message.save()

    def test_remove_old_messages(self):
        self.assertEqual(messages_number(), 150)
        remove_old_messages()
        self.assertEqual(messages_number(), 31)


class MessageFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/messages"
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
            profile=create_profile(
                user=self.lecturer_user, user_type=UserType.INSTRUCTOR
            )
        )

        self.student_messages = []
        for i in range(50):
            self.student_messages.append(
                create_message(
                    sender=self.lecturer_profile.profile,
                    recipient=self.profile.profile,
                    subject=f"subject{i}",
                    body=f"body{i}",
                    status=StatusType.NEW,
                )
            )

        self.lecturer_messages = []
        for i in range(100):
            self.lecturer_messages.append(
                create_message(
                    sender=self.profile.profile,
                    recipient=self.lecturer_profile.profile,
                    subject=f"subject{i}",
                    body=f"body{i}",
                    status=StatusType.NEW,
                )
            )

    def test_type_filter(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "type"
        variable = "SENT"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 100)
        values = list(
            set(
                [
                    str(self.profile.profile.uuid) == record["sender"]["id"]
                    for record in results
                ]
            )
        )
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_status_filter(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "status"
        variable = self.student_messages[0].status
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 150)
        values = list(set([variable in record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class MessageOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/messages"
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
            profile=create_profile(
                user=self.lecturer_user, user_type=UserType.INSTRUCTOR
            )
        )

        self.student_messages = []
        for i in range(50):
            self.student_messages.append(
                create_message(
                    sender=self.lecturer_profile.profile,
                    recipient=self.profile.profile,
                    subject=f"subject{i}",
                    body=f"body{i}",
                    status=StatusType.NEW,
                )
            )

        self.lecturer_messages = []
        for i in range(100):
            self.lecturer_messages.append(
                create_message(
                    sender=self.profile.profile,
                    recipient=self.lecturer_profile.profile,
                    subject=f"subject{i}",
                    body=f"body{i}",
                    status=StatusType.NEW,
                )
            )

        self.fields = ["sender", "recipient", "subject", "status", "created_at"]

    def test_ordering(self):
        for field in self.fields:
            login(self, self.data["email"], self.data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 150)
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
            elif "lessons_count" in field:
                field_values = [len(course["lessons"]) for course in results]
            elif "sender" in field or "recipient" in field:
                field_values = [course[field]["full_name"] for course in results]
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
            self.assertEqual(count, 150)
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
            elif "lessons_count" in field:
                field_values = [len(course["lessons"]) for course in results]
            elif "sender" in field or "recipient" in field:
                field_values = [course[field]["full_name"] for course in results]
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

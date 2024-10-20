from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_student_profile,
    create_lecturer_profile,
    create_notification,
)
from .helpers import login, notifications_number, is_float
from django.contrib import auth
import json
from notification.utils import remove_old_notifications, notify
from datetime import timedelta


class NotificationTest(APITestCase):
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

        self.student_notifications = []
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

            self.edit_data = {
                "title": self.student_notifications[0].title,
                "subtitle": self.student_notifications[0].subtitle,
                "description": self.student_notifications[0].description,
                "status": "READ",
                "path": self.student_notifications[0].path,
                "icon": self.student_notifications[0].icon,
            }

    def test_get_notifications_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_notifications_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 50)

    def test_edit_notification_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.put(
            f"{self.endpoint}/{self.student_notifications[0].id}", data=self.edit_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_notification_incorrect_user(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.put(
            f"{self.endpoint}/{self.student_notifications[0].id}", data=self.edit_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_notification_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.put(
            f"{self.endpoint}/{self.student_notifications[0].id}", data=self.edit_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(data["status"], self.edit_data["status"])


class NotificationUtilsTest(APITestCase):
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
            profile=create_profile(user=self.lecturer_user, user_type="W")
        )

        self.notifications = []
        for i in range(50):
            self.notifications.append(
                create_notification(
                    profile=self.profile.profile,
                    title=f"title_{i}",
                    subtitle=f"subtitle{i}",
                    description=f"description{i}",
                    status="READ",
                    path=f"path{i}",
                    icon=f"icon{i}",
                )
            )

        for i in range(100):
            self.notifications.append(
                create_notification(
                    profile=self.lecturer_profile.profile,
                    title=f"title_{i}",
                    subtitle=f"subtitle{i}",
                    description=f"description{i}",
                    status="READ",
                    path=f"path{i}",
                    icon=f"icon{i}",
                )
            )

        for index, notification in enumerate(self.notifications):
            notification.created_at = notification.created_at - timedelta(days=index)
            notification.save()

    def test_remove_old_notifications(self):
        self.assertEqual(notifications_number(), 150)
        remove_old_notifications()
        self.assertEqual(notifications_number(), 31)

    def test_notify(self):
        self.assertEqual(notifications_number(), 150)
        notify(
            profile=self.lecturer_profile.profile,
            title="test_title",
            subtitle="test_lesson",
            description="test_description",
            path="test_path",
            icon="test_icon",
        )
        self.assertEqual(notifications_number(), 151)


class NotificationOrderTest(APITestCase):
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

        self.student_notifications = []
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

        self.fields = ["created_at"]

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
            self.assertEqual(count, 50)
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
            self.assertEqual(count, 50)
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

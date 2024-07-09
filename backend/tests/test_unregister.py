from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_lecturer_profile,
    create_reservation,
    create_technology,
    create_lesson,
    create_schedule,
    create_purchase,
)
from .helpers import (
    users_number,
    login,
    is_user_found,
    profiles_number,
    emails_sent_number,
    get_schedule,
)
from django.contrib import auth
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class UnregisterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/unregister"
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
        self.user_2 = create_user(
            first_name="first_name_2",
            last_name="last_name_2",
            email="test_email_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.profile_2 = create_profile(user=self.user_2)
        self.lecturer_data = {
            "email": "lecturer_1@example.com",
            "password": "TestPassword123",
        }
        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.lecturer_data["email"],
            password=self.lecturer_data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(profile=create_profile(user=self.lecturer_user, user_type="W"))

        self.technology_1 = create_technology(name="Python")
        self.technology_2 = create_technology(name="JS")
        self.technology_3 = create_technology(name="VBA")

        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_1],
        )
        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_1],
        )
        self.lesson_3 = create_lesson(
            title="Python lesson 3",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_1],
        )
        self.lesson_4 = create_lesson(
            title="Python lesson 4",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_1],
        )

        self.lesson_1_purchase = create_purchase(
            lesson=self.lesson_1, student=self.profile, price=self.lesson_1.price
        )
        self.lesson_2_purchase = create_purchase(
            lesson=self.lesson_2, student=self.profile, price=self.lesson_2.price
        )
        self.lesson_3_purchase = create_purchase(
            lesson=self.lesson_3, student=self.profile, price=self.lesson_3.price
        )
        self.lesson_4_purchase = create_purchase(
            lesson=self.lesson_4, student=self.profile, price=self.lesson_4.price
        )

        self.past_schedule_1 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                - timedelta(days=5)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
            ),
            lesson=self.lesson_1,
        )
        self.past_schedule_2 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                - timedelta(days=15)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
            ),
        )
        self.future_schedule_1 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(days=5)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
            ),
            lesson=self.lesson_2,
        )
        self.future_schedule_2 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(days=15)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
            ),
        )

        self.past_reservation_1 = create_reservation(
            student=self.profile,
            lesson=self.lesson_1,
            schedule=self.past_schedule_1,
            purchase=self.lesson_1_purchase,
        )
        self.past_reservation_2 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_1,
            schedule=self.past_schedule_1,
            purchase=self.lesson_1_purchase,
        )
        self.future_reservation_1 = create_reservation(
            student=self.profile,
            lesson=self.lesson_2,
            schedule=self.future_schedule_1,
            purchase=self.lesson_2_purchase,
        )
        self.future_reservation_2 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_2,
            schedule=self.future_schedule_2,
            purchase=self.lesson_2_purchase,
        )

    def test_delete_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # delete
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(is_user_found(self.data["email"]))
        self.assertEqual(profiles_number(), 7)
        self.assertEqual(users_number(), 7)

    def test_delete_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(is_user_found(self.admin_data["email"]))
        self.assertEqual(profiles_number(), 7)
        self.assertEqual(users_number(), 7)

    def test_delete_authenticated_lecturer(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(is_user_found(self.lecturer_data["email"]))
        self.assertEqual(profiles_number(), 6)
        self.assertEqual(users_number(), 6)
        self.assertEqual(emails_sent_number(), 1)

    def test_delete_authenticated_student_1(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(is_user_found(self.data["email"]))
        self.assertEqual(profiles_number(), 6)
        self.assertEqual(users_number(), 6)
        self.assertEqual(emails_sent_number(), 1)
        self.assertTrue(get_schedule(self.future_schedule_1.id).lesson is None)

    def test_delete_authenticated_student_2(self):
        create_reservation(
            student=self.profile_2,
            lesson=self.lesson_2,
            schedule=self.future_schedule_1,
            purchase=self.lesson_2_purchase,
        )
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(is_user_found(self.data["email"]))
        self.assertEqual(profiles_number(), 6)
        self.assertEqual(users_number(), 6)
        self.assertEqual(emails_sent_number(), 0)

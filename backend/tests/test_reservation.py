from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_course,
    create_lesson_obj,
    create_technology_obj,
    create_skill_obj,
    create_topic_obj,
    create_purchase,
    create_schedule,
    create_teaching,
    create_reservation,
)
from .helpers import (
    login,
    reservation_number,
    is_reservation_found,
)
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class ReservationTest(APITestCase):
    def setUp(self):
        self.endpoint = "/reservation"
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
        self.user_3 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="user3@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.profile_1 = create_profile(user=self.user_1)
        self.profile_2 = create_profile(user=self.user_2)
        self.profile_3 = create_profile(user=self.user_3)

        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_profile(user=self.lecturer_user, user_type="W")

        self.course = create_course(
            title="course_title",
            description="course_description",
            technology=create_technology_obj(name="Python"),
            level="Podstawowy",
            price="99.99",
            github_url="www.example.com",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 1",
                    description="bbbb",
                    duration="90",
                    github_url="https://github.com/hackymatt/loop",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 2",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/loop",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 3",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/loop",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 4",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/loop",
                    price="2.99",
                ),
            ],
        )

        create_purchase(
            lesson=self.course.lessons.all()[0],
            student=self.profile_1,
            price=self.course.lessons.all()[0].price,
        )
        create_purchase(
            lesson=self.course.lessons.all()[1],
            student=self.profile_1,
            price=self.course.lessons.all()[1].price,
        )

        for lesson in self.course.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile,
                lesson=lesson,
                github_url="https://github.com/hackymatt/loop",
            )

        self.schedules = []
        for i in range(10):
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile,
                    time=make_aware(
                        datetime.now().replace(minute=15, second=0, microsecond=0)
                        + timedelta(minutes=15 * i)
                    ),
                )
            )

        self.reservation_1 = create_reservation(
            student=self.profile_1,
            lesson=self.course.lessons.all()[0],
            schedule=self.schedules[0],
        )
        self.reservation_2 = create_reservation(
            student=self.profile_1,
            lesson=self.course.lessons.all()[2],
            schedule=self.schedules[1],
        )

    def test_get_reservation_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_reservation_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_create_reservation_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course.lessons.all()[0].id,
            "schedule": self.schedules[2].id,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reservation_number(), 2)

    def test_create_reservation_authenticated_not_purchased(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course.lessons.all()[3].id,
            "schedule": self.schedules[2].id,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reservation_number(), 2)

    def test_create_reservation_authenticated_time_not_available(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course.lessons.all()[1].id,
            "schedule": self.schedules[1].id,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reservation_number(), 2)

    def test_create_reservation_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course.lessons.all()[1].id,
            "schedule": self.schedules[3].id,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reservation_number(), 3)

    def test_delete_reservation_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # delete data
        response = self.client.delete(f"{self.endpoint}/{self.reservation_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reservation_number(), 2)
        self.assertTrue(is_reservation_found(self.reservation_1.id))

    def test_delete_reservation_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete data
        response = self.client.delete(f"{self.endpoint}/{self.reservation_1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(reservation_number(), 1)
        self.assertFalse(is_reservation_found(self.reservation_1.id))

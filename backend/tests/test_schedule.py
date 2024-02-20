from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_course,
    create_lesson,
    create_technology,
    create_skill_obj,
    create_topic,
    create_schedule,
    create_teaching,
)
from .helpers import login, get_schedules
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class ScheduleTest(APITestCase):
    def setUp(self):
        self.endpoint = "/schedules"
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
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_profile(user=self.user_2)
        self.lecturer_data = {
            "email": "lecturer_1@example.com",
            "password": "TestPassword123",
        }
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.lecturer_data["email"],
            password=self.lecturer_data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )

        self.technology_1 = create_technology(name="Python")
        self.technology_2 = create_technology(name="JS")
        self.technology_3 = create_technology(name="VBA")

        # course 1
        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/hackymatt/lesson",
            price="9.99",
            technologies=[self.technology_1],
        )
        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/hackymatt/lesson",
            price="2.99",
            technologies=[self.technology_1],
        )

        self.topic_1 = create_topic(name="You will learn how to code")
        self.topic_2 = create_topic(name="You will learn a new IDE")

        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
            level="Podstawowy",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            lessons=[self.lesson_1, self.lesson_2],
        )

        for lesson in self.course_1.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile_1,
                lesson=lesson,
            )
            create_teaching(
                lecturer=self.lecturer_profile_2,
                lesson=lesson,
            )

        # course 2
        self.lesson_3 = create_lesson(
            title="JS lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/hackymatt/lesson",
            price="9.99",
            technologies=[self.technology_2],
        )
        self.lesson_4 = create_lesson(
            title="JS lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/hackymatt/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )
        self.lesson_5 = create_lesson(
            title="JS lesson 3",
            description="bbbb",
            duration="120",
            github_url="https://github.com/hackymatt/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )
        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            level="Zaawansowany",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            lessons=[self.lesson_3, self.lesson_4, self.lesson_5],
        )

        for lesson in self.course_2.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile_1,
                lesson=lesson,
            )
            create_teaching(
                lecturer=self.lecturer_profile_2,
                lesson=lesson,
            )

        # course 3
        self.lesson_6 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/hackymatt/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )
        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            level="Ekspert",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            lessons=[self.lesson_6],
        )

        for lesson in self.course_3.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile_1,
                lesson=lesson,
            )
            create_teaching(
                lecturer=self.lecturer_profile_2,
                lesson=lesson,
            )

        for i in range(10):
            create_schedule(
                lecturer=self.lecturer_profile_1,
                time=make_aware(
                    datetime.now().replace(minute=15, second=0, microsecond=0)
                    + timedelta(minutes=15 * i)
                ),
            )
            create_schedule(
                lecturer=self.lecturer_profile_2,
                time=make_aware(
                    datetime.now().replace(minute=15, second=0, microsecond=0)
                    + timedelta(minutes=15 * i)
                ),
            )

    def test_get_schedule_for_lesson_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?lesson_id={self.course_1.lessons.all()[0].id}&sort_by=time"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 20)

    def test_get_schedule_for_lesson_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?lesson_id={self.course_1.lessons.all()[0].id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 20)

    def test_create_schedule_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        available_times = [
            datetime.now().replace(second=0, microsecond=0) + timedelta(hours=i)
            for i in range(5)
        ]
        data = {
            "times": available_times,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_schedule_not_lecturer(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        available_times = [
            datetime.now().replace(second=0, microsecond=0) + timedelta(hours=i)
            for i in range(5)
        ]
        data = {
            "times": available_times,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_schedule_incorrect_time(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        available_times = [
            datetime.now().replace(minute=5 * i, second=0, microsecond=0)
            + timedelta(hours=i)
            for i in range(5)
        ]
        data = {
            "times": available_times,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_schedule(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        available_times = [
            datetime.now().replace(minute=15, second=0, microsecond=0)
            + timedelta(hours=i)
            for i in range(5)
        ]
        data = {
            "times": available_times,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(len(data), 5)
        times = [
            datetime.strptime(time["time"], "%Y-%m-%dT%H:%M:%fZ").strftime(
                "%Y-%m-%dT%H:%M"
            )
            for time in data
        ]
        self.assertEqual(
            times,
            [
                available_time.strftime("%Y-%m-%dT%H:%M")
                for available_time in available_times
            ],
        )

    def test_update_schedule(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        available_times = [
            datetime.now().replace(minute=15, second=0, microsecond=0)
            + timedelta(hours=i)
            for i in range(5)
        ]
        data = {
            "times": available_times
            + [
                get_schedules(
                    lecturer=self.lecturer_profile_1,
                )[0].time
            ],
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(len(data), 5)
        times = [
            datetime.strptime(time["time"], "%Y-%m-%dT%H:%M:%fZ").strftime(
                "%Y-%m-%dT%H:%M"
            )
            for time in data
        ]
        self.assertEqual(
            times,
            [
                available_time.strftime("%Y-%m-%dT%H:%M")
                for available_time in available_times
            ],
        )

    def test_delete_schedule(self):
        # no login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        available_times = []
        data = {
            "times": available_times,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)
        self.assertEqual(
            data,
            [],
        )

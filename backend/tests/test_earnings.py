from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_course,
    create_lesson,
    create_technology,
    create_skill,
    create_topic,
    create_purchase,
    create_schedule,
    create_teaching,
    create_reservation,
    create_finance,
    create_finance_history,
)
from .helpers import login
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from random import sample


class EarningsTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/earnings"
        self.data = {
            "email": "test_email@example.com",
            "password": "TestPassword123",
        }
        self.lecturer_data = {
            "email": "lecturer_1@example.com",
            "password": "TestPassword123",
        }
        self.admin_data = {
            "email": "admin@example.com",
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
        self.student_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.student_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="student_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
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
            password="TestPassword123",
            is_active=True,
        )
        self.student_profile_1 = create_profile(user=self.student_user_1)
        self.student_profile_2 = create_profile(user=self.student_user_2)
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )

        create_finance(
            lecturer=self.lecturer_profile_1,
            rate=150.00,
            commission=1,
        )

        create_finance(
            lecturer=self.lecturer_profile_2,
            account="48109024021679815769434176",
            rate=100,
            commission=5,
        )

        create_finance_history(
            lecturer=self.lecturer_profile_1,
            rate=150.00,
            commission=1,
        )

        create_finance_history(
            lecturer=self.lecturer_profile_2,
            account="48109024021679815769434176",
            rate=100,
            commission=5,
        )

        self.technology_1 = create_technology(name="Python")
        self.technology_2 = create_technology(name="JS")
        self.technology_3 = create_technology(name="VBA")

        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/hackymatt/lesson",
            price="99.99",
            technologies=[self.technology_1],
        )
        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/hackymatt/lesson",
            price="152.99",
            technologies=[self.technology_1],
        )
        self.lesson_3 = create_lesson(
            title="Python lesson 3",
            description="bbbb",
            duration="30",
            github_url="https://github.com/hackymatt/lesson",
            price="222.99",
            technologies=[self.technology_1],
        )
        self.lesson_4 = create_lesson(
            title="Python lesson 4",
            description="bbbb",
            duration="30",
            github_url="https://github.com/hackymatt/lesson",
            price="312.99",
            technologies=[self.technology_1],
        )

        self.topic_1 = create_topic(name="You will learn how to code")
        self.topic_2 = create_topic(name="You will learn a new IDE")

        self.skill_1 = create_skill(name="coding")
        self.skill_2 = create_skill(name="IDE")

        self.course = create_course(
            title="course_title",
            description="course_description",
            level="Podstawowy",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            lessons=[self.lesson_1, self.lesson_2, self.lesson_3, self.lesson_4],
        )

        for lesson in self.course.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile_1,
                lesson=lesson,
            )

        self.schedules = []
        for i in range(28):
            lessons = [self.lesson_1, self.lesson_2, self.lesson_3, self.lesson_4]
            schedule = create_schedule(
                lecturer=self.lecturer_profile_1,
                start_time=make_aware(
                    datetime.now().replace(
                        year=2024,
                        month=1,
                        day=1,
                        hour=0,
                        minute=0,
                        second=0,
                        microsecond=0,
                    )
                    + timedelta(days=i * 10, minutes=30 * i)
                ),
                end_time=make_aware(
                    datetime.now().replace(
                        year=2024,
                        month=1,
                        day=1,
                        hour=0,
                        minute=0,
                        second=0,
                        microsecond=0,
                    )
                    + timedelta(days=i * 10, minutes=30 * (i + 1))
                ),
                lesson=sample(lessons, 1)[0],
            )
            self.schedules.append(schedule)

        self.purchases = []
        self.reservations = []
        for i in range(14):
            lessons = [self.lesson_1, self.lesson_2, self.lesson_3, self.lesson_4]
            students = [self.student_profile_1, self.student_profile_2]
            prices = [
                self.lesson_1.price,
                self.lesson_2.price,
                self.lesson_3.price,
                self.lesson_4.price,
            ]
            schedules = self.schedules
            lesson = sample(lessons, 1)[0]
            student = sample(students, 1)[0]
            schedule = sample(schedules, 1)[0]
            purchase = create_purchase(
                lesson=lesson, student=student, price=sample(prices, 1)[0]
            )
            self.purchases.append(purchase)
            reservation = create_reservation(
                student=student, lesson=lesson, purchase=purchase, schedule=schedule
            )
            self.reservations.append(reservation)

    def test_get_earnings_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_earnings_lecturer(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        results = data["results"]
        count = data["records_count"]
        self.assertEqual(count, 9)
        sample = results[0]
        self.assertEqual(list(sample.keys()), ["actual", "year", "month", "earnings"])

    def test_get_earnings_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        results = data["results"]
        count = data["records_count"]
        self.assertEqual(count, 9)
        sample = results[0]
        self.assertEqual(
            list(sample.keys()), ["actual", "year", "month", "cost", "profit"]
        )

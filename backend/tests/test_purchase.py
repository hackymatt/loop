from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_course,
    create_lesson,
    create_technology_obj,
    create_skill_obj,
    create_topic_obj,
    create_purchase,
    create_teaching,
    create_schedule,
    create_reservation,
    create_review,
)
from .helpers import login
import json
from django.contrib import auth
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class PurchaseTest(APITestCase):
    def setUp(self):
        self.endpoint = "/purchase"
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
        self.profile = create_profile(user=self.user)

        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_profile(user=self.lecturer_user, user_type="W")

        # course 1
        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/hackymatt/lesson",
            price="9.99",
            technologies=[create_technology_obj(name="Python")],
        )
        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/hackymatt/lesson",
            price="2.99",
            technologies=[create_technology_obj(name="Python")],
        )
        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
            level="Podstawowy",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[self.lesson_1, self.lesson_2],
        )

        create_purchase(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile,
            price=self.course_1.lessons.all()[0].price,
        )

        create_purchase(
            lesson=self.course_1.lessons.all()[1],
            student=self.profile,
            price=self.course_1.lessons.all()[1].price,
        )

        for lesson in self.course_1.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile,
                lesson=lesson,
            )

        self.schedules = []
        for i in range(-10, 10):
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile,
                    time=make_aware(
                        datetime.now().replace(minute=15, second=0, microsecond=0)
                        + timedelta(minutes=15 * i)
                    ),
                )
            )

        create_reservation(
            student=self.profile,
            lesson=self.course_1.lessons.all()[0],
            schedule=self.schedules[len(self.schedules) - 3],
        )

        create_reservation(
            student=self.profile,
            lesson=self.course_1.lessons.all()[1],
            schedule=self.schedules[0],
        )

        # course 2
        self.lesson_3 = create_lesson(
            title="JS lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/hackymatt/lesson",
            price="9.99",
            technologies=[create_technology_obj(name="JS")],
        )
        self.lesson_4 = create_lesson(
            title="JS lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/hackymatt/lesson",
            price="2.99",
            technologies=[create_technology_obj(name="JS")],
        )
        self.lesson_5 = create_lesson(
            title="JS lesson 3",
            description="bbbb",
            duration="120",
            github_url="https://github.com/hackymatt/lesson",
            price="2.99",
            technologies=[create_technology_obj(name="JS")],
        )
        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            level="Zaawansowany",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[self.lesson_3, self.lesson_4, self.lesson_5],
        )

        create_purchase(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile,
            price=self.course_2.lessons.all()[0].price,
        )
        create_purchase(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile,
            price=self.course_2.lessons.all()[1].price,
        )

        create_review(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )

        # course 3
        self.lesson_6 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/hackymatt/lesson",
            price="9.99",
            technologies=[create_technology_obj(name="VBA")],
        )
        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            level="Ekspert",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[self.lesson_6],
        )

    def test_get_purchase_unauthenticated(self):
        # login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_purchase_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        self.assertEqual(records_count, 4)

    def test_create_purchase_unauthenticated(self):
        # login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course_3.lessons.all()[0].id,
            "price": self.course_1.lessons.all()[0].price,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_purchase_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course_3.lessons.all()[0].id,
            "price": self.course_1.lessons.all()[0].price,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

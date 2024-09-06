from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_student_profile,
    create_course,
    create_lesson,
    create_technology,
    create_skill,
    create_topic,
    create_module,
)
from .helpers import login
from django.contrib import auth
from unittest.mock import patch


class ThrottlingTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/courses"
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

        self.technology_1 = create_technology(name="Python")
        self.technology_2 = create_technology(name="JS")
        self.technology_3 = create_technology(name="VBA")

        # course 1
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

        self.topic_1 = create_topic(name="You will learn how to code")
        self.topic_2 = create_topic(name="You will learn a new IDE")

        self.skill_1 = create_skill(name="coding")
        self.skill_2 = create_skill(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
        )

        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
            level="Podstawowy",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            modules=[self.module_1],
        )

        # course 2
        self.lesson_3 = create_lesson(
            title="JS lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_2],
        )
        self.lesson_4 = create_lesson(
            title="JS lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )
        self.lesson_5 = create_lesson(
            title="JS lesson 3",
            description="bbbb",
            duration="120",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )

        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_3, self.lesson_4, self.lesson_5]
        )

        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            level="Zaawansowany",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            modules=[self.module_2],
        )

        # course 3
        self.lesson_6 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )
        self.module_3 = create_module(title="Module 3", lessons=[self.lesson_6])

        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            level="Ekspert",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            modules=[self.module_3],
        )

        self.user_rate = 100

    @patch("rest_framework.throttling.UserRateThrottle.get_rate", lambda x: "100/hour")
    def test_throttling_user(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        for _ in range(self.user_rate):
            response = self.client.get(self.endpoint)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

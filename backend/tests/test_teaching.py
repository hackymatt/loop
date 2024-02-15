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
    create_teaching,
)
from .helpers import login
from django.contrib import auth
import json


class TeachingTest(APITestCase):
    def setUp(self):
        self.endpoint = "/teaching"
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
        self.profile = create_profile(user=self.user, user_type="W")

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

        self.teaching = []
        for lesson in self.course_1.lessons.all():
            self.teaching.append(
                create_teaching(
                    lecturer=self.profile,
                    lesson=lesson,
                )
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

        self.teaching.append(
            create_teaching(
                lecturer=self.profile,
                lesson=self.course_2.lessons.all()[1],
            )
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

        self.teaching.append(
            create_teaching(
                lecturer=self.profile,
                lesson=self.course_3.lessons.all()[0],
            )
        )

    def test_get_teaching_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_teaching_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 4)

    def test_add_to_teaching_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        data = {
            "lesson": self.course_2.lessons.all()[0].id,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_to_teaching_single_lesson_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = {
            "lesson": self.course_2.lessons.all()[0].id,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(len(data), 5)

    def test_add_to_teaching_whole_course_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = {
            "course": self.course_2.id,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(len(data), 6)

    def test_delete_single_lesson_from_teaching(self):
        # no login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = {"lesson": self.course_1.lessons.all()[0].id}
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

    def test_delete_whole_course_from_teaching(self):
        # no login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        data = {"course": self.course_1.id}
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

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
)
from .helpers import login
import json
from django.contrib import auth


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

        # course 1
        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
            technology=create_technology_obj(name="Python"),
            level="Podstawowy",
            price="99.99",
            github_url="https://github.com/hackymatt/course",
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
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 2",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="2.99",
                ),
            ],
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

        # course 2
        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            technology=create_technology_obj(name="Javascript"),
            level="Zaawansowany",
            price="300",
            github_url="https://github.com/hackymatt/course",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 1",
                    description="bbbb",
                    duration="90",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 2",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 3",
                    description="bbbb",
                    duration="120",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="2.99",
                ),
            ],
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

        # course 3
        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            technology=create_technology_obj(name="VBA"),
            level="Ekspert",
            price="220",
            github_url="https://github.com/hackymatt/course",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[
                create_lesson_obj(
                    id=-1,
                    title="VBA lesson 1",
                    description="bbbb",
                    duration="90",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="9.99",
                ),
            ],
        )

        create_purchase(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile,
            price=self.course_3.lessons.all()[0].price,
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
        self.assertEqual(records_count, 5)

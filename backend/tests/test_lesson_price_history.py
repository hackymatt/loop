from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_lesson,
    create_lesson_obj,
    create_technology_obj,
    create_review,
    create_purchase,
    create_teaching,
    create_lesson_price_history,
)
from .helpers import (
    login,
    is_data_match,
    get_user,
    get_profile,
    get_lesson,
    filter_dict,
    get_technology,
    lessons_number,
)
from django.contrib import auth
import json


class LessonPriceHistoryTest(APITestCase):
    def setUp(self):
        self.endpoint = "/lesson-price-history"
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
        self.course = create_course(
            title="course_title",
            description="course_description",
            level="Podstawowy",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[self.lesson_1, self.lesson_2],
        )

        create_course_price_history(self.course, 80)
        create_course_price_history(self.course, 100)
        create_course_price_history(self.course, 120)
        create_lesson_price_history(self.lesson_1, 15)
        create_lesson_price_history(self.lesson_1, 25)
        create_lesson_price_history(self.lesson_1, 5)
        create_lesson_price_history(self.lesson_2, 1)
        create_lesson_price_history(self.lesson_2, 5)
        create_lesson_price_history(self.lesson_2, 3)

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
        self.course_2 = create_course(
            title="course_title 2",
            description="course_description",
            level="Podstawowy",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[self.lesson_3, self.lesson_4],
        )

        create_course_price_history(self.course_2, 120)
        create_course_price_history(self.course_2, 100)
        create_course_price_history(self.course_2, 80)
        create_lesson_price_history(self.lesson_3, 15)
        create_lesson_price_history(self.lesson_3, 25)
        create_lesson_price_history(self.lesson_3, 5)
        create_lesson_price_history(self.lesson_4, 1)
        create_lesson_price_history(self.lesson_4, 5)
        create_lesson_price_history(self.lesson_4, 3)

        self.lesson_5 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/hackymatt/lesson",
            price="9.99",
            technologies=[create_technology_obj(name="VBA")],
        )
        self.lesson_6 = create_lesson(
            title="VBA lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/hackymatt/lesson",
            price="2.99",
            technologies=[create_technology_obj(name="VBA")],
        )
        self.course_3 = create_course(
            title="course_title 3",
            description="course_description",
            level="Podstawowy",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[self.lesson_5, self.lesson_6],
        )

        create_course_price_history(self.course_3, 100)
        create_course_price_history(self.course_3, 80)
        create_course_price_history(self.course_3, 120)
        create_lesson_price_history(self.lesson_5, 15)
        create_lesson_price_history(self.lesson_5, 25)
        create_lesson_price_history(self.lesson_5, 5)
        create_lesson_price_history(self.lesson_6, 1)
        create_lesson_price_history(self.lesson_6, 5)
        create_lesson_price_history(self.lesson_6, 3)

    def test_get_lesson_price_history_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_lesson_price_history_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_lesson_price_history_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 18)
        prices = [record["price"] for record in results]
        self.assertEqual(
            prices,
            [
                "15.00",
                "25.00",
                "5.00",
                "1.00",
                "5.00",
                "3.00",
                "15.00",
                "25.00",
                "5.00",
                "1.00",
            ],
        )

from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_admin_profile,
    create_student_profile,
    create_lecturer_profile,
    create_course,
    create_lesson,
    create_skill,
    create_topic,
    create_review,
    create_purchase,
    create_lesson_price_history,
    create_schedule,
    create_technology,
    create_teaching,
    create_reservation,
    create_finance_history,
    create_coupon,
    create_coupon_user,
    create_newsletter,
    create_meeting,
    create_module,
    create_certificate,
    create_notification,
    create_message,
)
from .helpers import login
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from const import CANCELLATION_TIME
import uuid


def is_float(element: any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


class CourseOrderTest(APITestCase):
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
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W")
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

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

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
        )

        self.review_course_1_1 = create_review(
            lesson=self.lesson_1,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.lesson_1,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.lesson_2,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
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

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_4.price,
        )
        create_purchase(
            lesson=self.lesson_3,
            student=self.profile_2,
            price=self.lesson_3.price,
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile_2,
            price=self.lesson_4.price,
        )
        create_purchase(
            lesson=self.lesson_5,
            student=self.profile_2,
            price=self.lesson_5.price,
        )

        self.review_course_2_1 = create_review(
            lesson=self.lesson_3,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_2_2 = create_review(
            lesson=self.lesson_4,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_2_3 = create_review(
            lesson=self.lesson_3,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=2,
            review="So so lesson.",
        )
        self.review_course_2_4 = create_review(
            lesson=self.lesson_4,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=1,
            review="So so lesson.",
        )
        self.review_course_2_5 = create_review(
            lesson=self.lesson_5,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="So so lesson.",
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

        create_purchase(
            lesson=self.lesson_6,
            student=self.profile,
            price=self.lesson_6.price,
        )
        create_purchase(
            lesson=self.lesson_6,
            student=self.profile_2,
            price=self.lesson_6.price,
        )

        self.review_course_3_1 = create_review(
            lesson=self.lesson_6,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_3_2 = create_review(
            lesson=self.lesson_6,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=2,
            review="So so lesson.",
        )

        self.fields = [
            "title",
            "level",
            "price",
            "duration",
            "rating",
            "students_count",
        ]

    def test_ordering(self):
        for field in self.fields:
            # no login
            self.assertFalse(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 3)
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
            self.assertEqual(count, 3)
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


class ReviewOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/reviews"
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
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W")
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

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

        self.review_course_1_1 = create_review(
            lesson=self.lesson_1,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.lesson_1,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.lesson_2,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
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

        self.review_course_2_1 = create_review(
            lesson=self.lesson_3,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_2_2 = create_review(
            lesson=self.lesson_4,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_2_3 = create_review(
            lesson=self.lesson_3,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=2,
            review="So so lesson.",
        )
        self.review_course_2_4 = create_review(
            lesson=self.lesson_4,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=1,
            review="So so lesson.",
        )
        self.review_course_2_5 = create_review(
            lesson=self.lesson_5,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="So so lesson.",
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

        self.review_course_3_1 = create_review(
            lesson=self.lesson_6,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_3_2 = create_review(
            lesson=self.lesson_6,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=2,
            review="So so lesson.",
        )

        self.fields = ["created_at"]

    def test_ordering(self):
        for field in self.fields:
            # no login
            self.assertFalse(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 10)
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
            self.assertEqual(count, 10)
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


class ScheduleOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/schedules"
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
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )
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
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W")
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

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

        for i in range(10):
            create_schedule(
                lecturer=self.lecturer_profile_1,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (i + 1))
                ),
            )
            create_schedule(
                lecturer=self.lecturer_profile_2,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (i + 1))
                ),
            )

        self.fields = ["start_time"]

    def test_ordering(self):
        for field in self.fields:
            # login
            login(self, self.lecturer_data["email"], self.lecturer_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 10)
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
            self.assertEqual(count, 10)
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


class LessonPriceHistoryOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/lesson-price-history"
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
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )

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

        self.topic_1 = create_topic(name="You will learn how to code")
        self.topic_2 = create_topic(name="You will learn a new IDE")

        self.skill_1 = create_skill(name="coding")
        self.skill_2 = create_skill(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
        )

        self.course = create_course(
            title="course_title",
            description="course_description",
            level="Podstawowy",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            modules=[self.module_1],
        )

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

        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_3, self.lesson_4]
        )

        self.course_2 = create_course(
            title="course_title 2",
            description="course_description",
            level="Podstawowy",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            modules=[self.module_2],
        )

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
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )
        self.lesson_6 = create_lesson(
            title="VBA lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_3],
        )

        self.module_3 = create_module(
            title="Module 3", lessons=[self.lesson_5, self.lesson_6]
        )

        self.course_3 = create_course(
            title="course_title 3",
            description="course_description",
            level="Podstawowy",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            modules=[self.module_3],
        )

        create_lesson_price_history(self.lesson_6, 15)
        create_lesson_price_history(self.lesson_6, 25)
        create_lesson_price_history(self.lesson_6, 5)
        create_lesson_price_history(self.lesson_6, 1)
        create_lesson_price_history(self.lesson_6, 5)
        create_lesson_price_history(self.lesson_6, 3)

        self.fields = ["lesson_name", "price", "created_at"]

    def test_ordering(self):
        for field in self.fields:
            # login
            login(self, self.admin_data["email"], self.admin_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 18)
            if field == "lesson_name":
                field_values = [course["lesson"]["title"] for course in results]
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
            self.assertEqual(count, 18)
            if field == "lesson_name":
                field_values = [course["lesson"]["title"] for course in results]
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


class BestTechnologyOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/best-technologies"
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
        create_technology(name="Python")
        create_technology(name="JavaScript")
        create_technology(name="C++")
        create_technology(name="C#")
        create_technology(name="VBA")

        self.fields = ["name", "courses_count"]

    def test_ordering(self):
        for field in self.fields:
            self.assertFalse(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 5)
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
            self.assertEqual(count, 5)
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


class TechnologyOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/technologies"
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
        create_technology(name="Python")
        create_technology(name="JavaScript")
        create_technology(name="C++")
        create_technology(name="C#")
        create_technology(name="VBA")

        self.fields = ["name", "created_at"]

    def test_ordering(self):
        for field in self.fields:
            self.assertFalse(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 5)
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
            self.assertEqual(count, 5)
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


class TopicOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/topics"
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
        create_topic(name="A")
        create_topic(name="B")
        create_topic(name="C")
        create_topic(name="D")
        create_topic(name="E")

        self.fields = ["name", "created_at"]

    def test_ordering(self):
        for field in self.fields:
            self.assertFalse(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 5)
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
            self.assertEqual(count, 5)
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


class SkillOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/skills"
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
        create_skill(name="A")
        create_skill(name="B")
        create_skill(name="C")
        create_skill(name="D")
        create_skill(name="E")

        self.fields = ["name", "created_at"]

    def test_ordering(self):
        for field in self.fields:
            self.assertFalse(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 5)
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
            self.assertEqual(count, 5)
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


class LecturerOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/lecturers"
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
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W"),
            title="Engineer",
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W"),
            title="DevOps",
        )

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

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
        )

        self.review_course_1_1 = create_review(
            lesson=self.lesson_1,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.lesson_1,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.lesson_2,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
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

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_4.price,
        )
        create_purchase(
            lesson=self.lesson_3,
            student=self.profile_2,
            price=self.lesson_3.price,
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile_2,
            price=self.lesson_4.price,
        )
        create_purchase(
            lesson=self.lesson_5,
            student=self.profile_2,
            price=self.lesson_5.price,
        )

        self.review_course_2_1 = create_review(
            lesson=self.lesson_3,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_2_2 = create_review(
            lesson=self.lesson_4,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_2_3 = create_review(
            lesson=self.lesson_3,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=2,
            review="So so lesson.",
        )
        self.review_course_2_4 = create_review(
            lesson=self.lesson_4,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=1,
            review="So so lesson.",
        )
        self.review_course_2_5 = create_review(
            lesson=self.lesson_5,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="So so lesson.",
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

        create_purchase(
            lesson=self.lesson_6,
            student=self.profile,
            price=self.lesson_6.price,
        )
        create_purchase(
            lesson=self.lesson_6,
            student=self.profile_2,
            price=self.lesson_6.price,
        )

        self.review_course_3_1 = create_review(
            lesson=self.lesson_6,
            student=self.profile,
            lecturer=self.lecturer_profile_2,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_3_2 = create_review(
            lesson=self.lesson_6,
            student=self.profile_2,
            lecturer=self.lecturer_profile_2,
            rating=2,
            review="So so lesson.",
        )

        create_teaching(lecturer=self.lecturer_profile_1, lesson=self.lesson_1)
        create_teaching(lecturer=self.lecturer_profile_1, lesson=self.lesson_2)
        create_teaching(lecturer=self.lecturer_profile_1, lesson=self.lesson_3)
        create_teaching(lecturer=self.lecturer_profile_2, lesson=self.lesson_4)
        create_teaching(lecturer=self.lecturer_profile_2, lesson=self.lesson_5)

        self.fields = ["rating", "full_name", "title"]

    def test_ordering(self):
        for field in self.fields:
            # no login
            self.assertFalse(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 2)
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
            self.assertEqual(count, 2)
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


class PurchaseOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/purchase"
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
        self.profile = create_student_profile(profile=create_profile(user=self.user))

        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
        )

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

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
        )

        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
        )

        for module in self.course_1.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile,
                    lesson=lesson,
                )

        self.schedules = []
        for i in range(-100, 10):
            schedule = create_schedule(
                lecturer=self.lecturer_profile,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (i + 1))
                ),
            )
            if (schedule.start_time - make_aware(datetime.now())) < timedelta(
                hours=CANCELLATION_TIME
            ):
                id = str(uuid.uuid4())
                schedule.meeting = create_meeting(
                    event_id=id, url=f"https://example.com/{id}"
                )
                schedule.save()

            self.schedules.append(schedule)
        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_1,
            schedule=self.schedules[len(self.schedules) - 3],
            purchase=self.purchase_1,
        )
        self.purchase_2 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_2,
            schedule=self.schedules[0],
            purchase=self.purchase_2,
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

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_4.price,
        )

        create_review(
            lesson=self.lesson_3,
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

        self.fields = [
            "lesson_title",
            "lesson_status",
            "review_status",
            "lecturer_id",
            "created_at",
        ]

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
            self.assertEqual(count, 6)
            if "_title" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course["reservation"]
                    for course in results
                    if course["reservation"] is not None
                ]
                parent_objects = [
                    course["schedule"]
                    for course in parent_objects
                    if course["schedule"] is not None
                ]
                parent_objects = [
                    course[field1]
                    for course in parent_objects
                    if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
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
            self.assertEqual(count, 6)
            if "_title" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course["reservation"]
                    for course in results
                    if course["reservation"] is not None
                ]
                parent_objects = [
                    course["schedule"]
                    for course in parent_objects
                    if course["schedule"] is not None
                ]
                parent_objects = [
                    course[field1]
                    for course in parent_objects
                    if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
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


class LessonOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/lessons"
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
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )
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
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W")
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

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

        create_lesson_price_history(self.lesson_1, 15)
        create_lesson_price_history(self.lesson_1, 25)
        create_lesson_price_history(self.lesson_1, 5)
        create_lesson_price_history(self.lesson_2, 1)
        create_lesson_price_history(self.lesson_2, 5)
        create_lesson_price_history(self.lesson_2, 3)

        create_teaching(
            lesson=self.lesson_1,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_2,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_1,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_2,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
        )

        self.review_1 = create_review(
            lesson=self.lesson_1,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.lesson_1,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_3 = create_review(
            lesson=self.lesson_2,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

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

        create_lesson_price_history(self.lesson_3, 15)
        create_lesson_price_history(self.lesson_3, 25)
        create_lesson_price_history(self.lesson_3, 5)
        create_lesson_price_history(self.lesson_4, 1)
        create_lesson_price_history(self.lesson_4, 5)
        create_lesson_price_history(self.lesson_4, 3)

        create_teaching(
            lesson=self.lesson_3,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_4,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_3,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_4,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_4.price,
        )

        self.review_4 = create_review(
            lesson=self.lesson_3,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_5 = create_review(
            lesson=self.lesson_4,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        self.lesson_5 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )

        self.lesson_6 = create_lesson(
            title="VBA lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lasson",
            price="2.99",
            technologies=[self.technology_3],
        )

        create_lesson_price_history(self.lesson_5, 15)
        create_lesson_price_history(self.lesson_5, 25)
        create_lesson_price_history(self.lesson_5, 5)
        create_lesson_price_history(self.lesson_6, 1)
        create_lesson_price_history(self.lesson_6, 5)
        create_lesson_price_history(self.lesson_6, 3)

        create_teaching(
            lesson=self.lesson_5,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_6,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_5,
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.lesson_6,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_5,
            student=self.profile,
            price=self.lesson_5.price,
        )
        create_purchase(
            lesson=self.lesson_6,
            student=self.profile,
            price=self.lesson_6.price,
        )

        self.review_6 = create_review(
            lesson=self.lesson_5,
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_7 = create_review(
            lesson=self.lesson_6,
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        self.fields = ["title", "duration", "price", "github_url", "active"]

    def test_ordering(self):
        for field in self.fields:
            login(self, self.admin_data["email"], self.admin_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 6)
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
            self.assertEqual(count, 6)
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


class TeachingOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/teaching"
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
        self.profile = create_lecturer_profile(
            profile=create_profile(user=self.user, user_type="W")
        )

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

        self.teaching = []
        for module in self.course_1.modules.all():
            for lesson in module.lessons.all():
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

        self.teaching.append(
            create_teaching(
                lecturer=self.profile,
                lesson=self.lesson_4,
            )
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

        self.teaching.append(
            create_teaching(
                lecturer=self.profile,
                lesson=self.lesson_6,
            )
        )

        self.fields = ["title", "duration", "price", "github_url", "active"]

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
            self.assertEqual(count, 6)
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
            self.assertEqual(count, 6)
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


class UsersOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/users"
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
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )
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
        self.student_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="student_1@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.student_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="student_2@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.student_profile_1 = create_student_profile(
            profile=create_profile(user=self.student_user_1)
        )
        self.student_profile_2 = create_student_profile(
            profile=create_profile(user=self.student_user_2)
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W")
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

        self.fields = [
            "first_name",
            "last_name",
            "email",
            "active",
            "gender",
            "user_type",
            "created_at",
            "phone_number",
            "dob",
            "street_address",
            "zip_code",
            "city",
            "country",
        ]

    def test_ordering(self):
        for field in self.fields:
            login(self, self.admin_data["email"], self.admin_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 8)
            field_values = [user[field] for user in results]
            field_values = [value for value in field_values if value is not None]
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
            self.assertEqual(count, 8)
            field_values = [user[field] for user in results]
            field_values = [value for value in field_values if value is not None]
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


class FinanceHistoryOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/finance-history"
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
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )
        self.student_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
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
        self.student_profile = create_profile(user=self.student_user)
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W")
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

        self.finance_1 = create_finance_history(
            lecturer=self.lecturer_profile_1,
            account="48109024021679815769434175",
            rate=150.00,
            commission=1,
        )

        self.finance_2 = create_finance_history(
            lecturer=self.lecturer_profile_2,
            account="48109024021679815769434176",
            rate=100,
            commission=5,
        )

        self.fields = [
            "lecturer_id",
            "account",
            "rate",
            "commission",
            "created_at",
        ]

    def test_ordering(self):
        for field in self.fields:
            login(self, self.admin_data["email"], self.admin_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 2)
            if "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course[field1] for course in results if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
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
            self.assertEqual(count, 2)
            if "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course[field1] for course in results if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
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


class CouponOrderingTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/coupons"
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
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )
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

        self.coupon = create_coupon(
            code="aaaaaaa",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )
        create_coupon(
            code="aaaaaab",
            discount=11,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=11)),
        )
        create_coupon(
            code="aaaaaav",
            discount=12,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=22)),
        )
        create_coupon(
            code="aaaaaad",
            discount=14,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=False,
            expiration_date=make_aware(datetime.now() + timedelta(days=33)),
        )
        create_coupon(
            code="aaaaaae",
            discount=41,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=4)),
        )
        create_coupon(
            code="aaaaaag",
            discount=4,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=False,
            expiration_date=make_aware(datetime.now() + timedelta(days=5)),
        )

        self.fields = [
            "code",
            "discount",
            "active",
            "expiration_date",
        ]

    def test_ordering(self):
        for field in self.fields:
            login(self, self.admin_data["email"], self.admin_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 6)
            if "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course[field1] for course in results if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
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
            self.assertEqual(count, 6)
            if "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course[field1] for course in results if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
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


class CouponUserOrderingTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/coupon-usage"
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
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )
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

        self.coupon_1 = create_coupon(
            code="aaaaaaa",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
        )
        self.coupon_2 = create_coupon(
            code="aaaaaab",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=11)),
        )
        self.coupon_3 = create_coupon(
            code="aaaaaav",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=22)),
        )
        create_coupon(
            code="aaaaaad",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=33)),
        )
        create_coupon(
            code="aaaaaae",
            discount=10,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=4)),
        )
        create_coupon(
            code="aaaaaag",
            discount=10,
            is_infinite=False,
            all_users=True,
            is_percentage=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=5)),
        )

        self.coupon_user_1 = create_coupon_user(self.coupon_1, self.profile)
        self.coupon_user_2 = create_coupon_user(self.coupon_2, self.profile)
        self.coupon_user_3 = create_coupon_user(self.coupon_3, self.profile)

        self.fields = [
            "coupon_code",
            "user_email",
            "created_at",
        ]

    def test_ordering(self):
        for field in self.fields:
            login(self, self.admin_data["email"], self.admin_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 3)
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
            self.assertEqual(count, 3)
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


class NewsletterEntriesOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/newsletter"

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
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )

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

        self.active_newsletters = [
            create_newsletter(email=f"test_active_{i}@example.com") for i in range(15)
        ]
        self.inactive_newsletters = [
            create_newsletter(email=f"test_inactive_{i}@example.com", active=False)
            for i in range(5)
        ]

        self.fields = [
            "uuid",
            "email",
            "active",
            "created_at",
        ]

    def test_ordering(self):
        for field in self.fields:
            login(self, self.admin_data["email"], self.admin_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 20)
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
            self.assertEqual(count, 20)
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


class ModuleOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/modules"
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
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )
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
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile_1 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_1, user_type="W")
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

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

        self.module_1 = create_module(title="Module 1", lessons=[self.lesson_1])

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

        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_3, self.lesson_4]
        )

        self.lesson_5 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )

        self.lesson_6 = create_lesson(
            title="VBA lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_3],
        )

        self.module_3 = create_module(
            title="Module 3", lessons=[self.lesson_5, self.lesson_6, self.lesson_2]
        )

        self.fields = ["title", "lessons_count"]

    def test_ordering(self):
        for field in self.fields:
            login(self, self.admin_data["email"], self.admin_data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 3)
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
            self.assertEqual(count, 3)
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


class CertificateOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/certificates"
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
        self.profile_1 = create_student_profile(
            profile=create_profile(user=self.user_1)
        )
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )
        self.profile_3 = create_student_profile(
            profile=create_profile(user=self.user_3)
        )

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
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
        )

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

        self.topic_1 = create_topic(name="You will learn how to code")
        self.topic_2 = create_topic(name="You will learn a new IDE")

        self.skill_1 = create_skill(name="coding")
        self.skill_2 = create_skill(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
        )
        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_3, self.lesson_4]
        )

        self.course = create_course(
            title="course_title",
            description="course_description",
            level="Podstawowy",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            modules=[self.module_1, self.module_2],
        )

        for module in self.course.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile,
                    lesson=lesson,
                )

        self.schedules = []
        for i in range(10):
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile,
                    start_time=make_aware(
                        datetime.now().replace(minute=30, second=0, microsecond=0)
                        + timedelta(minutes=30 * i)
                    ),
                    end_time=make_aware(
                        datetime.now().replace(minute=30, second=0, microsecond=0)
                        + timedelta(minutes=30 * (i + 1))
                    ),
                )
            )

        self.schedules.append(
            create_schedule(
                lecturer=self.lecturer_profile,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * 100)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (100 + 1))
                ),
            )
        )

        self.schedules.append(
            create_schedule(
                lecturer=self.lecturer_profile,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * 102)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (102 + 1))
                ),
            )
        )

        self.schedules.append(
            create_schedule(
                lecturer=self.lecturer_profile,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * 103)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (103 + 1))
                ),
            )
        )
        self.long_timeslot = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 50)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 53)
            ),
            lesson=self.lesson_1,
        )
        self.long_timeslot_2 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 30)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 33)
            ),
            lesson=self.lesson_1,
        )

        self.long_timeslot_3 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 400)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 403)
            ),
            lesson=self.lesson_4,
        )

        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile_1,
            price=self.lesson_1.price,
        )
        self.reservation_1 = create_reservation(
            student=self.profile_1,
            lesson=self.lesson_1,
            schedule=self.schedules[0],
            purchase=self.purchase_1,
        )
        self.schedules[0].lesson = self.lesson_1
        self.schedules[0].save()
        self.purchase_2 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile_2,
            price=self.lesson_2.price,
        )
        self.reservation_2 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_2,
            schedule=self.schedules[2],
            purchase=self.purchase_2,
        )
        self.schedules[2].lesson = self.lesson_2
        self.schedules[2].save()
        self.purchase_3 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile_2,
            price=self.lesson_1.price,
        )
        self.reservation_3 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_1,
            schedule=self.schedules[0],
            purchase=self.purchase_3,
        )
        self.purchase_4 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile_1,
            price=self.lesson_2.price,
        )
        self.reservation_4 = create_reservation(
            student=self.profile_1,
            lesson=self.lesson_2,
            schedule=self.schedules[6],
            purchase=self.purchase_4,
        )
        self.schedules[6].lesson = self.lesson_2
        self.schedules[6].save()
        self.purchase_5 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile_2,
            price=self.lesson_2.price,
        )
        self.reservation_5 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_2,
            schedule=self.long_timeslot_2,
            purchase=self.purchase_5,
        )
        self.long_timeslot_2.lesson = self.lesson_1
        self.long_timeslot_2.save()
        self.purchase_6 = create_purchase(
            lesson=self.lesson_4,
            student=self.profile_1,
            price=self.lesson_4.price,
        )
        self.reservation_6 = create_reservation(
            student=self.profile_1,
            lesson=self.lesson_4,
            schedule=self.long_timeslot_3,
            purchase=self.purchase_6,
        )
        self.long_timeslot_3.lesson = self.lesson_4
        self.long_timeslot_3.save()

        self.certificate = create_certificate(
            entity_type="L",
            entity=self.lesson_1,
            student=self.profile_1,
        )
        self.certificate_2 = create_certificate(
            entity_type="M",
            entity=self.module_1,
            student=self.profile_1,
        )

        self.fields = ["title", "type", "completed_at"]

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
            self.assertEqual(count, 2)
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
            self.assertEqual(count, 2)
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


class MessageOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/messages"
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

        self.student_messages = []
        for i in range(50):
            self.student_messages.append(
                create_message(
                    sender=self.lecturer_profile.profile,
                    recipient=self.profile.profile,
                    subject=f"subject{i}",
                    body=f"body{i}",
                    status="NEW",
                )
            )

        self.lecturer_messages = []
        for i in range(100):
            self.lecturer_messages.append(
                create_message(
                    sender=self.profile.profile,
                    recipient=self.lecturer_profile.profile,
                    subject=f"subject{i}",
                    body=f"body{i}",
                    status="NEW",
                )
            )

        self.fields = ["sender", "recipient", "subject", "status", "created_at"]

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
            self.assertEqual(count, 150)
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
            elif "sender" in field or "recipient" in field:
                field_values = [course[field]["full_name"] for course in results]
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
            self.assertEqual(count, 150)
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
            elif "sender" in field or "recipient" in field:
                field_values = [course[field]["full_name"] for course in results]
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

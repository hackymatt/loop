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
    create_teaching,
    create_schedule,
    create_lesson_price_history,
    create_reservation,
    create_technology,
    create_finance,
    create_finance_history,
    create_coupon,
    create_coupon_user,
    create_newsletter,
    create_meeting,
    create_module,
    create_certificate,
    create_notification,
    create_message,
    create_payment,
)
from .helpers import login
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from random import sample
from config_global import CANCELLATION_TIME
import uuid


class CourseFilterTest(APITestCase):
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
            price="99.99",
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
            payment=create_payment(amount=self.lesson_1.price),
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
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
            price="299.99",
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

        create_teaching(
            lesson=self.lesson_3,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_4,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_5,
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
        create_teaching(
            lesson=self.lesson_5,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_4.price,
            payment=create_payment(amount=self.lesson_4.price),
        )
        create_purchase(
            lesson=self.lesson_3,
            student=self.profile_2,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile_2,
            price=self.lesson_4.price,
            payment=create_payment(amount=self.lesson_4.price),
        )
        create_purchase(
            lesson=self.lesson_5,
            student=self.profile_2,
            price=self.lesson_5.price,
            payment=create_payment(amount=self.lesson_5.price),
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
            price="109.99",
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

        create_teaching(
            lesson=self.lesson_6,
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.lesson_6,
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.lesson_6,
            student=self.profile,
            price=self.lesson_6.price,
            payment=create_payment(amount=self.lesson_6.price),
        )
        create_purchase(
            lesson=self.lesson_6,
            student=self.profile_2,
            price=self.lesson_6.price,
            payment=create_payment(amount=self.lesson_6.price),
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

    def test_search_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?search=JS lesson 1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 1)

    def test_rating_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?rating_from=3.5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_duration_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?filters=(duration_to=100)|(duration_from=250)"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 1)

    def test_lecturer_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        ids = ",".join(
            [
                str(self.lecturer_profile_1.id),
                str(self.lecturer_profile_2.id),
            ]
        )
        response = self.client.get(f"{self.endpoint}?lecturer_in={ids}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 3)

    def test_technology_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?technology_in=Python,VBA")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_level_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?level_in=Podstawowy,Ekspert")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_price_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}")
        response = self.client.get(f"{self.endpoint}?price_from=100&price_to=300")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_active_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?active=False")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 0)


class ReviewFilterTest(APITestCase):
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

    def test_course_id_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?course_id={self.course_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 3)

    def test_lesson_id_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?lesson_id={self.lesson_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_lecturer_id_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?lecturer_id={self.lecturer_profile_1.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 10)

    def test_lecturer_uuid_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?lecturer_uuid={self.lecturer_profile_1.profile.uuid}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 10)

    def test_rating_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?rating=4")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 3)

    def test_rating_from_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?rating_from=4.5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 3)

    def test_rating_to_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?rating_to=4")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 7)


class ScheduleFilterTest(APITestCase):
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
        create_finance(lecturer=self.lecturer_profile_1, rate=150, commission=0)
        create_finance(lecturer=self.lecturer_profile_2, rate=120, commission=10)

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

        for module in self.course_1.modules.all():
            for lesson in module.lessons.all():
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

        for module in self.course_2.modules.all():
            for lesson in module.lessons.all():
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

        for module in self.course_3.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile_1,
                    lesson=lesson,
                )
                create_teaching(
                    lecturer=self.lecturer_profile_2,
                    lesson=lesson,
                )

        self.schedules = []
        for i in range(50):
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile_1,
                    start_time=make_aware(
                        datetime.now().replace(
                            hour=0, minute=30, second=0, microsecond=0
                        )
                        + timedelta(minutes=30 * (i + 10))
                    ),
                    end_time=make_aware(
                        datetime.now().replace(
                            hour=0, minute=30, second=0, microsecond=0
                        )
                        + timedelta(minutes=30 * (i + 11))
                    ),
                    lesson=self.lesson_1,
                )
            )
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile_2,
                    start_time=make_aware(
                        datetime.now().replace(
                            hour=0, minute=30, second=0, microsecond=0
                        )
                        + timedelta(minutes=30 * (i + 10))
                    ),
                    end_time=make_aware(
                        datetime.now().replace(
                            hour=0, minute=30, second=0, microsecond=0
                        )
                        + timedelta(minutes=30 * (i + 11))
                    ),
                )
            )
        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_1,
            schedule=self.schedules[0],
            purchase=self.purchase_1,
        )
        self.schedules[0].lesson = self.lesson_1
        self.schedules[0].save()
        self.purchase_2 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_2,
            schedule=self.schedules[1],
            purchase=self.purchase_2,
        )
        self.schedules[1].lesson = self.lesson_2
        self.schedules[1].save()

    def test_reserved_filter(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?reserved=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 50)

    def test_lesson_id_filter(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?lesson_id={self.lesson_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 50)

    def test_lecturer_id_filter(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?lecturer_id={self.lecturer_profile_1.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 50)

    def test_time_from_filter(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        time = str(self.schedules[0].start_time)[0:10]
        response = self.client.get(f"{self.endpoint}?time_from={time}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 50)

    def test_time_to_filter(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        time = str(self.schedules[len(self.schedules) - 1].start_time)[0:10]
        response = self.client.get(f"{self.endpoint}?time_to={time}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 37)

    def test_time_filter(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        time = str(self.schedules[len(self.schedules) - 1].start_time)[0:10]
        response = self.client.get(f"{self.endpoint}?time={time}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 13)

    def test_duration_filter(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?duration=60")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 50)


class LessonDatesFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/lesson-dates"
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

        for module in self.course_1.modules.all():
            for lesson in module.lessons.all():
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

        for module in self.course_2.modules.all():
            for lesson in module.lessons.all():
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

        for module in self.course_3.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile_1,
                    lesson=lesson,
                )
                create_teaching(
                    lecturer=self.lecturer_profile_2,
                    lesson=lesson,
                )

        self.schedules = []

        date_48_hours_ago = datetime.now().replace(
            minute=30, second=0, microsecond=0
        ) - timedelta(hours=48)

        for i in range(150):
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile_1,
                    start_time=make_aware(date_48_hours_ago + timedelta(hours=30 * i)),
                    end_time=make_aware(
                        date_48_hours_ago + timedelta(hours=30 * (i + 1))
                    ),
                )
            )
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile_2,
                    start_time=make_aware(date_48_hours_ago + timedelta(hours=30 * i)),
                    end_time=make_aware(
                        date_48_hours_ago + timedelta(hours=30 * (i + 1))
                    ),
                )
            )

    def test_lesson_id_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?lesson_id={self.lesson_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 147)

    def test_lecturer_id_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?lecturer_id={self.lecturer_profile_1.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 147)

    def test_year_month_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        time = str(self.schedules[len(self.schedules) - 1].start_time)[0:7]
        response = self.client.get(f"{self.endpoint}?year_month={time}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertNotEqual(count, 0)

    def test_duration_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?duration=60")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 147)


class LessonPriceHistoryFilterTest(APITestCase):
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

        create_lesson_price_history(self.lesson_5, 15)
        create_lesson_price_history(self.lesson_5, 25)
        create_lesson_price_history(self.lesson_5, 5)
        create_lesson_price_history(self.lesson_6, 1)
        create_lesson_price_history(self.lesson_6, 5)
        create_lesson_price_history(self.lesson_6, 3)

    def test_lesson_name_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        title = self.lesson_1.title[0:5]
        response = self.client.get(f"{self.endpoint}?lesson_name={title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 6)
        titles = list(set([title in record["lesson"]["title"] for record in results]))
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0])

    def test_price_from_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 5
        response = self.client.get(f"{self.endpoint}?price_from={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 12)
        prices = list(set([float(record["price"]) >= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_price_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 10
        response = self.client.get(f"{self.endpoint}?price_to={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 12)
        prices = list(set([float(record["price"]) <= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_created_at_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        date = str(self.lesson_1.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?created_at={date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 18)
        dates = list(set([date in record["created_at"] for record in results]))
        self.assertTrue(len(dates) == 1)
        self.assertTrue(dates[0])


class TechnologyFilterTest(APITestCase):
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
        self.technology = create_technology(name="Python")
        self.technology_2 = create_technology(name="JavaScript")
        create_technology(name="C++")
        create_technology(name="C#")
        create_technology(name="VBA")

        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology],
        )
        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
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

    def test_name_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?name=Python")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        prices = [record["name"] for record in results]
        self.assertEqual(prices, ["Python"])

    def test_courses_count_from_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?courses_count_from=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        self.assertEqual(records_count, 2)

    def test_created_at_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        date = str(self.technology.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?created_at={date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        dates = list(set([date in record["created_at"] for record in results]))
        self.assertTrue(len(dates) == 1)
        self.assertTrue(dates[0])


class TopicFilterTest(APITestCase):
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
        self.topic = create_topic(name="A")
        create_topic(name="B")
        create_topic(name="C")
        create_topic(name="D")
        create_topic(name="E")

    def test_name_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?name=A")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        prices = [record["name"] for record in results]
        self.assertEqual(prices, ["A"])

    def test_created_at_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        date = str(self.topic.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?created_at={date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        dates = list(set([date in record["created_at"] for record in results]))
        self.assertTrue(len(dates) == 1)
        self.assertTrue(dates[0])


class SkillFilterTest(APITestCase):
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
        self.skill = create_skill(name="A")
        create_skill(name="B")
        create_skill(name="C")
        create_skill(name="D")
        create_skill(name="E")

    def test_name_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?name=A")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        prices = [record["name"] for record in results]
        self.assertEqual(prices, ["A"])

    def test_created_at_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        date = str(self.skill.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?created_at={date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        dates = list(set([date in record["created_at"] for record in results]))
        self.assertTrue(len(dates) == 1)
        self.assertTrue(dates[0])


class LecturerFilterTest(APITestCase):
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

        self.course = create_course(
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
            payment=create_payment(amount=self.lesson_1.price),
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
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
            lecturer=self.lecturer_profile_2,
            rating=3,
            review="So so lesson.",
        )

    def test_search_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?search=lecturer_1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 1)

    def test_id_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?id={self.lecturer_profile_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        ids = [record["id"] for record in results]
        self.assertEqual(ids, [self.lecturer_profile_1.id])

    def test_uuid_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?uuid={self.lecturer_profile_1.profile.uuid}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        ids = [record["id"] for record in results]
        self.assertEqual(ids, [self.lecturer_profile_1.id])

    def test_rating_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?rating_from=4")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        ratings = [record["rating"] for record in results]
        self.assertEqual(ratings, [4.5])


class PurchaseFilterTest(APITestCase):
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
        self.lesson_3 = create_lesson(
            title="Python lesson 3",
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
            title="Module 1", lessons=[self.lesson_1, self.lesson_2, self.lesson_3]
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
            payment=create_payment(amount=self.lesson_1.price),
        )

        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
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
            payment=create_payment(amount=self.lesson_1.price),
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
            payment=create_payment(amount=self.lesson_2.price),
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_2,
            schedule=self.schedules[0],
            purchase=self.purchase_2,
        )
        self.purchase_3 = create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_3,
            schedule=self.schedules[1],
            purchase=self.purchase_3,
        )

        create_review(
            lesson=self.lesson_2,
            student=self.profile,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )

        # course 2
        self.lesson_4 = create_lesson(
            title="JS lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_2],
        )
        self.lesson_5 = create_lesson(
            title="JS lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )
        self.lesson_6 = create_lesson(
            title="JS lesson 3",
            description="bbbb",
            duration="120",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )

        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_4, self.lesson_5, self.lesson_6]
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
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_purchase(
            lesson=self.lesson_5,
            student=self.profile,
            price=self.lesson_4.price,
            payment=create_payment(amount=self.lesson_4.price),
        )

        create_review(
            lesson=self.lesson_4,
            student=self.profile,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )

        # course 3
        self.lesson_7 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )

        self.module_3 = create_module(title="Module 3", lessons=[self.lesson_7])

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

    def test_lesson_title_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        lesson_title = self.lesson_1.title[1:5]
        response = self.client.get(f"{self.endpoint}?lesson_title={lesson_title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 6)
        titles = list(
            set([lesson_title in record["lesson"]["title"] for record in results])
        )
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0])

    def test_lesson_status_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        lesson_status = "potwierdzona"
        response = self.client.get(f"{self.endpoint}?lesson_status={lesson_status}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        statuses = list(
            set([record["lesson_status"] == lesson_status for record in results])
        )
        self.assertTrue(len(statuses) == 1)
        self.assertTrue(statuses[0])

    def test_review_status_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        review_status = "oczekujące"
        response = self.client.get(f"{self.endpoint}?review_status={review_status}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        statuses = list(
            set([record["review_status"] == review_status for record in results])
        )
        self.assertTrue(len(statuses) == 1)
        self.assertTrue(statuses[0])

    def test_review_status_exclude_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        review_status = "brak"
        response = self.client.get(
            f"{self.endpoint}?review_status_exclude={review_status}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        statuses = list(
            set([record["review_status"] == review_status for record in results])
        )
        self.assertTrue(len(statuses) == 1)
        self.assertFalse(statuses[0])

    def test_lecturer_id_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        id = self.lecturer_profile.id
        response = self.client.get(f"{self.endpoint}?lecturer_id={id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        ids = list(
            set(
                [
                    str(record["reservation"]["schedule"]["lecturer"]["id"]) == str(id)
                    for record in results
                ]
            )
        )
        self.assertTrue(len(ids) == 1)
        self.assertTrue(ids[0])

    def test_created_at_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        date = str(self.course_1.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?created_at={date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 8)
        dates = list(set([date in record["created_at"] for record in results]))
        self.assertTrue(len(dates) == 1)
        self.assertTrue(dates[0])


class LessonFilterTest(APITestCase):
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
            payment=create_payment(amount=self.lesson_1.price),
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
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
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_4.price,
            payment=create_payment(amount=self.lesson_4.price),
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
            payment=create_payment(amount=self.lesson_5.price),
        )
        create_purchase(
            lesson=self.lesson_6,
            student=self.profile,
            price=self.lesson_6.price,
            payment=create_payment(amount=self.lesson_6.price),
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

    def test_title_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        title = "pyth"
        response = self.client.get(f"{self.endpoint}?title={title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        titles = list(set([title in record["title"].lower() for record in results]))
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0])

    def test_duration_from_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        duration = 40
        response = self.client.get(f"{self.endpoint}?duration_from={duration}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        durations = list(set([record["duration"] >= duration for record in results]))
        self.assertTrue(len(durations) == 1)
        self.assertTrue(durations[0])

    def test_duration_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        duration = 30
        response = self.client.get(f"{self.endpoint}?duration_to={duration}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        durations = list(set([record["duration"] <= duration for record in results]))
        self.assertTrue(len(durations) == 1)
        self.assertTrue(durations[0])

    def test_price_from_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 5
        response = self.client.get(f"{self.endpoint}?price_from={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        prices = list(set([float(record["price"]) >= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_price_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 10
        response = self.client.get(f"{self.endpoint}?price_to={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 6)
        prices = list(set([float(record["price"]) <= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_github_url_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        github_url = "lesson"
        response = self.client.get(f"{self.endpoint}?github_url={github_url}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        github_urls = list(
            set([github_url in record["github_url"] for record in results])
        )
        self.assertTrue(len(github_urls) == 1)
        self.assertTrue(github_urls[0])

    def test_active_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        self.lesson_5.active = True
        self.lesson_5.save()

        active = "True"
        response = self.client.get(f"{self.endpoint}?active={active}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        actives = list(set([record["active"] for record in results]))
        self.assertTrue(len(actives) == 1)
        self.assertTrue(actives[0])


class ManageTeachingFilterTest(APITestCase):
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

    def test_title_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        title = "pyth"
        response = self.client.get(f"{self.endpoint}?title={title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        titles = list(set([title in record["title"].lower() for record in results]))
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0])

    def test_duration_from_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        duration = 40
        response = self.client.get(f"{self.endpoint}?duration_from={duration}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 4)
        durations = list(set([record["duration"] >= duration for record in results]))
        self.assertTrue(len(durations) == 1)
        self.assertTrue(durations[0])

    def test_duration_to_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        duration = 30
        response = self.client.get(f"{self.endpoint}?duration_to={duration}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        durations = list(set([record["duration"] <= duration for record in results]))
        self.assertTrue(len(durations) == 1)
        self.assertTrue(durations[0])

    def test_price_from_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 5
        response = self.client.get(f"{self.endpoint}?price_from={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        prices = list(set([float(record["price"]) >= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_price_to_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 10
        response = self.client.get(f"{self.endpoint}?price_to={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 6)
        prices = list(set([float(record["price"]) <= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_github_url_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        github_url = "lesson"
        response = self.client.get(f"{self.endpoint}?github_url={github_url}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 6)
        github_urls = list(
            set([github_url in record["github_url"] for record in results])
        )
        self.assertTrue(len(github_urls) == 1)
        self.assertTrue(github_urls[0])

    def test_active_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        self.lesson_5.active = True
        self.lesson_5.save()

        active = "True"
        response = self.client.get(f"{self.endpoint}?active={active}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        actives = list(set([record["active"] for record in results]))
        self.assertTrue(len(actives) == 1)
        self.assertTrue(actives[0])

    def test_teaching_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        self.lesson_5.active = True
        self.lesson_5.save()

        teaching = "True"
        response = self.client.get(f"{self.endpoint}?teaching={teaching}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 4)
        teachings = list(set([record["teaching"] for record in results]))
        self.assertTrue(len(teachings) == 1)
        self.assertTrue(teachings[0])


class TeachingFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/lesson-lecturers"
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

    def test_lesson_id_filter(self):
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        id = self.lesson_1.id
        response = self.client.get(f"{self.endpoint}?lesson_id={id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)


class UsersFilterTest(APITestCase):
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
            profile=create_profile(user=self.lecturer_user_1, user_type="W"),
            title="soft",
        )
        self.lecturer_profile_2 = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user_2, user_type="W")
        )

    def test_first_name_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "first_name"
        variable = "first"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_last_name_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "last_name"
        variable = "last"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_email_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "email"
        variable = "student_2"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_active_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "active"
        variable = "true"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 8)
        values = list(set([True == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_gender_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "gender"
        variable = "m"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_user_type_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "user_type"
        variable = "w"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_created_at_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "created_at"
        variable = str(self.admin_profile.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 8)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_phone_number_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "phone_number"
        variable = "123"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_dob_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "dob"
        variable = "1999"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_street_address_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "street_address"
        variable = "tree"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_zip_code_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "zip_code"
        variable = "zip"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_city_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "city"
        variable = "ty"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_country_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "country"
        variable = "try"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class FinanceHistoryFilterTest(APITestCase):
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
            rate=150.00,
            commission=1,
        )

        self.finance_2 = create_finance_history(
            lecturer=self.lecturer_profile_2,
            account="48109024021679815769434176",
            rate=100,
            commission=5,
        )

    def test_lecturer_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "lecturer_id"
        variable = self.lecturer_profile_1.id
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable == record["lecturer"]["id"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_account_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "account"
        variable = "48"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_rate_from_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "rate_from"
        variable = "120"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable <= record["rate"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_rate_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "rate_to"
        variable = "120"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable >= record["rate"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_commission_from_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "commission_from"
        variable = 2
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable <= record["commission"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_commission_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "commission_to"
        variable = 2
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable >= record["commission"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_created_at_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "created_at"
        variable = str(self.finance_1.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        values = list(set([variable in record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class CouponFilteringTest(APITestCase):
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

    def test_code_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "code"
        variable = str(self.coupon.code)
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable in record[column].lower() for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_active_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "active"
        variable = True
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 4)
        values = list(set([variable == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_discount_from_from_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "discount_from"
        variable = 10
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 5)
        values = list(set([variable <= record["discount"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_discount_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "discount_to"
        variable = 10
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        values = list(set([variable >= record["discount"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_expiration_date_to_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "expiration_date_to"
        variable = str(self.coupon.expiration_date)[0:10]
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        values = list(
            set([variable >= record["expiration_date"] for record in results])
        )
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class CouponUserFilteringTest(APITestCase):
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

    def test_user_id_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "user_id"
        variable = self.coupon_user_1.user.id
        response = self.client.get(f"{self.endpoint}")
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        values = list(set([variable == record["user"]["id"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_coupon_code_filter(self):
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "coupon_code"
        variable = self.coupon_1.code
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(
            set([variable in record["coupon"]["code"].lower() for record in results])
        )
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class EarningsFilterTest(APITestCase):
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
        self.admin_profile = create_admin_profile(
            profile=create_profile(user=self.admin_user, user_type="A")
        )
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
            github_url="https://github.com/loopedupl/lesson",
            price="99.99",
            technologies=[self.technology_1],
        )
        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="152.99",
            technologies=[self.technology_1],
        )
        self.lesson_3 = create_lesson(
            title="Python lesson 3",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="222.99",
            technologies=[self.technology_1],
        )
        self.lesson_4 = create_lesson(
            title="Python lesson 4",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="312.99",
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
            price = sample(prices, 1)[0]
            purchase = create_purchase(
                lesson=lesson,
                student=student,
                price=price,
                payment=create_payment(amount=price),
            )
            self.purchases.append(purchase)
            reservation = create_reservation(
                student=student, lesson=lesson, purchase=purchase, schedule=schedule
            )
            self.reservations.append(reservation)

    def test_filter_company_earnings(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?total=True")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        results = data["results"]
        count = data["records_count"]
        self.assertEqual(count, 9)
        sample = results[0]
        self.assertEqual(
            list(sample.keys()), ["actual", "year", "month", "cost", "profit"]
        )

    def test_filter_lecturers_earnings(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?total=False")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        results = data["results"]
        count = data["records_count"]
        self.assertEqual(count, 9)
        sample = results[0]
        self.assertEqual(
            list(sample.keys()), ["lecturer", "actual", "year", "month", "earnings"]
        )

    def test_filter_year(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "year"
        variable = str(self.purchases[0].created_at)[0:4]
        variable = int(variable)
        response = self.client.get(f"{self.endpoint}?total=False&{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 9)
        values = list(set([variable == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_filter_month(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "month"
        variable = str(self.reservations[0].schedule.end_time)[5:7]
        if variable[0] == "0":
            variable = variable[1]
        variable = int(variable)
        response = self.client.get(f"{self.endpoint}?total=False&{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_filter_lecturer(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "lecturer"
        variable = self.lecturer_profile_1.id
        response = self.client.get(f"{self.endpoint}?total=False&{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 9)
        values = list(set([variable == record[column]["id"] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class NewsletterEntriesFilterTest(APITestCase):
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

    def test_id_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "uuid"
        variable = str(self.active_newsletters[0].uuid)
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_email_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "email"
        variable = "test_active"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 15)
        values = list(set([variable in record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_active_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "active"
        variable = True
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 15)
        values = list(set([variable == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_created_at_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "created_at"
        variable = str(self.active_newsletters[0].created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 20)
        values = list(set([variable in record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class ModuleFilterTest(APITestCase):
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

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
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
            title="Module 3", lessons=[self.lesson_5, self.lesson_6]
        )

    def test_title_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "title"
        variable = str(self.module_1.title)
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class CertificateFilterTest(APITestCase):
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
            payment=create_payment(amount=self.lesson_1.price),
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
            payment=create_payment(amount=self.lesson_2.price),
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
            payment=create_payment(amount=self.lesson_1.price),
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
            payment=create_payment(amount=self.lesson_2.price),
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
            payment=create_payment(amount=self.lesson_2.price),
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
            payment=create_payment(amount=self.lesson_4.price),
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

    def test_title_filter(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "title"
        variable = str(self.certificate.title)
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable == record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_type_filter(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "type"
        variable = "L"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable == record[column][0] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_completed_at_filter(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "completed_at"
        variable = str(self.certificate.created_at - timedelta(days=1))[0:10]
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        values = list(set([variable in record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class NotificationFilterTest(APITestCase):
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

        self.student_notifications = [
            create_notification(
                profile=self.profile.profile,
                title=f"title",
                subtitle=f"subtitle",
                description=f"description",
                status="READ",
                path=f"path",
                icon=f"icon",
            )
        ]
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

    def test_status_filter(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "status"
        variable = self.student_notifications[0].status
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        values = list(set([variable in record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])


class MessageFilterTest(APITestCase):
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

    def test_type_filter(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "type"
        variable = "SENT"
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 100)
        values = list(
            set(
                [
                    str(self.profile.profile.uuid) == record["sender"]["id"]
                    for record in results
                ]
            )
        )
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

    def test_status_filter(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        column = "status"
        variable = self.student_messages[0].status
        response = self.client.get(f"{self.endpoint}?{column}={variable}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 150)
        values = list(set([variable in record[column] for record in results]))
        self.assertTrue(len(values) == 1)
        self.assertTrue(values[0])

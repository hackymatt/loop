from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase
from unittest.mock import patch
from .factory import (
    create_user,
    create_profile,
    create_student_profile,
    create_lecturer_profile,
    create_course,
    create_lesson,
    create_technology,
    create_tag,
    create_topic,
    create_review,
    create_purchase,
    create_reservation,
    create_teaching,
    create_schedule,
    create_meeting,
    create_module,
    create_payment,
)
from .helpers import (
    login,
    reviews_number,
    is_data_match,
    get_review,
    is_review_found,
    mock_send_message,
    notifications_number,
    is_float,
)
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from review.utils import remind_review
from utils.google.gmail import GmailApi


class ReviewTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/reviews"
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

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

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
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            modules=[self.module_1, self.module_2],
        )

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile_1,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile_1,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )
        create_purchase(
            lesson=self.lesson_3,
            student=self.profile_1,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )

        self.review_1 = create_review(
            lesson=self.lesson_1,
            student=self.profile_1,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.lesson_1,
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Super helpful.",
        )
        self.review_3 = create_review(
            lesson=self.lesson_1,
            student=self.profile_3,
            lecturer=self.lecturer_profile,
            rating=4,
            review="Great lesson.",
        )
        self.review_4 = create_review(
            lesson=self.lesson_2,
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=2,
            review="Terrible.",
        )
        self.review_5 = create_review(
            lesson=self.lesson_2,
            student=self.profile_3,
            lecturer=self.lecturer_profile,
            rating=5,
        )

    def test_get_reviews_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 5)

    def test_get_reviews_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 5)

    def test_get_course_reviews_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?course_id={self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 5)

    def test_get_course_reviews_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?course_id={self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 5)

    def test_create_review_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_1.id,
            "lecturer": self.lecturer_profile.id,
            "rating": 3,
            "review": "Good lesson.",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reviews_number(), 5)
        self.assertEqual(notifications_number(), 0)

    def test_create_review_authenticated_not_purchased(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_4.id,
            "lecturer": self.lecturer_profile.id,
            "rating": 3,
            "review": "Good lesson.",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reviews_number(), 5)
        self.assertEqual(notifications_number(), 0)

    def test_create_review_authenticated_already_created(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_1.id,
            "lecturer": self.lecturer_profile.id,
            "rating": 3,
            "review": "Good lesson.",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reviews_number(), 5)
        self.assertEqual(notifications_number(), 0)

    def test_create_review_authenticated_incorrect_rating(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_1.id,
            "lecturer": self.lecturer_profile.id,
            "rating": 3.4,
            "review": "Good lesson.",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reviews_number(), 5)
        self.assertEqual(notifications_number(), 0)

    def test_create_review_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_3.id,
            "lecturer": self.lecturer_profile.id,
            "rating": 3.5,
            "review": "Good lesson.",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reviews_number(), 6)
        self.assertEqual(notifications_number(), 1)

    def test_update_review_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_1.id,
            "lecturer": self.lecturer_profile.id,
            "rating": 3,
            "review": "Good lesson.",
        }
        response = self.client.put(f"{self.endpoint}/{self.review_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reviews_number(), 5)

    def test_update_review_authenticated_not_owner(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_3.id,
            "lecturer": self.lecturer_profile.id,
            "rating": 4,
            "review": "Good lesson.",
        }
        response = self.client.put(f"{self.endpoint}/{self.review_2.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reviews_number(), 5)

    def test_update_review_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_1.id,
            "lecturer": self.lecturer_profile.id,
            "rating": 4,
            "review": "Good lesson.",
        }
        response = self.client.put(f"{self.endpoint}/{self.review_1.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = json.loads(response.content)
        self.assertEqual(reviews_number(), 5)
        lesson = results.pop("lesson")
        lecturer = results.pop("lecturer")
        self.assertTrue(is_data_match(get_review(self.review_1.id), results))
        self.assertEqual(lesson, get_review(self.review_1.id).lesson.id)
        self.assertEqual(lecturer, self.review_1.lecturer.id)

    def test_delete_review_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # delete data
        response = self.client.delete(f"{self.endpoint}/{self.review_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reviews_number(), 5)
        self.assertTrue(is_review_found(self.review_1.id))

    def test_delete_review_authenticated_not_owner(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete data
        response = self.client.delete(f"{self.endpoint}/{self.review_2.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reviews_number(), 5)
        self.assertTrue(is_review_found(self.review_1.id))

    def test_delete_review_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete data
        response = self.client.delete(f"{self.endpoint}/{self.review_1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(reviews_number(), 4)
        self.assertFalse(is_review_found(self.review_1.id))


class BestReviewTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/best-reviews"
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

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2, self.lesson_3]
        )

        self.course = create_course(
            title="course_title",
            description="course_description",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            modules=[self.module_1],
        )

        self.review_1 = create_review(
            lesson=self.lesson_1,
            student=self.profile_1,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.lesson_1,
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Super helpful.",
        )
        self.review_3 = create_review(
            lesson=self.lesson_1,
            student=self.profile_3,
            lecturer=self.lecturer_profile,
            rating=4,
            review="Great lesson.",
        )
        self.review_4 = create_review(
            lesson=self.lesson_2,
            student=self.profile_1,
            lecturer=self.lecturer_profile,
            rating=3,
        )
        self.review_5 = create_review(
            lesson=self.lesson_2,
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=2,
            review="Terrible.",
        )
        self.review_6 = create_review(
            lesson=self.lesson_2,
            student=self.profile_3,
            lecturer=self.lecturer_profile,
            rating=5,
        )

    def test_get_best_reviews_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_get_best_reviews_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)


class ReviewStatsTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/reviews-stats"
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

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

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
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            modules=[self.module_1, self.module_2],
        )

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile_1,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile_1,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )
        create_purchase(
            lesson=self.lesson_3,
            student=self.profile_1,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )

        self.review_1 = create_review(
            lesson=self.lesson_1,
            student=self.profile_1,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.lesson_1,
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Super helpful.",
        )
        self.review_3 = create_review(
            lesson=self.lesson_1,
            student=self.profile_3,
            lecturer=self.lecturer_profile,
            rating=4,
            review="Great lesson.",
        )
        self.review_4 = create_review(
            lesson=self.lesson_2,
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=2,
            review="Terrible.",
        )
        self.review_5 = create_review(
            lesson=self.lesson_2,
            student=self.profile_3,
            lecturer=self.lecturer_profile,
            rating=5,
        )

    def test_get_reviews_stats_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        results = data["results"]
        self.assertEqual(count, 3)
        self.assertEqual(
            results,
            [
                {"rating": "2.0", "count": 1},
                {"rating": "4.0", "count": 1},
                {"rating": "5.0", "count": 3},
            ],
        )

    def test_get_reviews_stats_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        results = data["results"]
        self.assertEqual(count, 3)
        self.assertEqual(
            results,
            [
                {"rating": "2.0", "count": 1},
                {"rating": "4.0", "count": 1},
                {"rating": "5.0", "count": 3},
            ],
        )

    def test_get_reviews_stats_course_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?course_id={self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        results = data["results"]
        self.assertEqual(count, 3)
        self.assertEqual(
            results,
            [
                {"rating": "2.0", "count": 1},
                {"rating": "4.0", "count": 1},
                {"rating": "5.0", "count": 3},
            ],
        )

    def test_get_reviews_stats_course_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?course_id={self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        results = data["results"]
        self.assertEqual(count, 3)
        self.assertEqual(
            results,
            [
                {"rating": "2.0", "count": 1},
                {"rating": "4.0", "count": 1},
                {"rating": "5.0", "count": 3},
            ],
        )


class ReviewConfirmationTest(TestCase):
    def setUp(self):
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
        self.profile = create_student_profile(profile=create_profile(user=self.user))
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )
        self.profile_3 = create_student_profile(
            profile=create_profile(user=self.user_3)
        )

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

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
        )

        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
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

        for module in self.course_1.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile,
                    lesson=lesson,
                )

        self.schedules = []
        for i in range(-72, 10):
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile,
                    start_time=make_aware(datetime.now() + timedelta(minutes=30 * i)),
                    end_time=make_aware(
                        datetime.now() + timedelta(minutes=30 * (i + 1))
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
            schedule=self.schedules[len(self.schedules) - 3],
            purchase=self.purchase_1,
        )
        create_reservation(
            student=self.profile_2,
            lesson=self.lesson_1,
            schedule=self.schedules[len(self.schedules) - 3],
            purchase=self.purchase_1,
        )
        create_reservation(
            student=self.profile_3,
            lesson=self.lesson_1,
            schedule=self.schedules[len(self.schedules) - 3],
            purchase=self.purchase_1,
        )
        self.schedules[len(self.schedules) - 3].lesson = self.lesson_1
        self.meeting_1 = create_meeting(event_id="abc1", url="abc1")
        self.schedules[len(self.schedules) - 3].meeting = self.meeting_1
        self.schedules[len(self.schedules) - 3].save()
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
        create_reservation(
            student=self.profile_2,
            lesson=self.lesson_2,
            schedule=self.schedules[0],
            purchase=self.purchase_2,
        )
        create_review(
            lesson=self.lesson_2,
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )
        self.meeting_2 = create_meeting(event_id="abc2", url="abc2")
        self.schedules[0].lesson = self.lesson_2
        self.schedules[0].meeting = self.meeting_2
        self.schedules[0].save()

    @patch.object(GmailApi, "_send_message")
    def test_review_reminder(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        self.assertEqual(reviews_number(), 1)
        remind_review()
        self.assertEqual(_send_message_mock.call_count, 1)
        self.assertEqual(notifications_number(), 1)


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

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
        )

        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
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
            tags=[self.tag_1, self.tag_2],
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
            tags=[self.tag_1, self.tag_2],
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

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
        )

        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
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
            tags=[self.tag_1, self.tag_2],
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
            tags=[self.tag_1, self.tag_2],
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

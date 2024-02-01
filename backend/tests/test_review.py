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
    create_review,
    create_purchase,
)
from .helpers import (
    login,
    get_user,
    get_profile,
    reviews_number,
    is_data_match,
    get_review,
    is_review_found,
)
from django.contrib import auth
import json


class ReviewTest(APITestCase):
    def setUp(self):
        self.endpoint = "/reviews"
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
        self.profile_1 = create_profile(user=self.user_1)
        self.profile_2 = create_profile(user=self.user_2)
        self.profile_3 = create_profile(user=self.user_3)

        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_profile(user=self.lecturer_user, user_type="W")

        self.course = create_course(
            title="course_title",
            description="course_description",
            technology=[create_technology_obj(name="Python")],
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
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 3",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 4",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="2.99",
                ),
            ],
        )

        create_purchase(
            lesson=self.course.lessons.all()[0],
            student=self.profile_1,
            price=self.course.lessons.all()[0].price,
        )
        create_purchase(
            lesson=self.course.lessons.all()[1],
            student=self.profile_1,
            price=self.course.lessons.all()[1].price,
        )
        create_purchase(
            lesson=self.course.lessons.all()[2],
            student=self.profile_1,
            price=self.course.lessons.all()[2].price,
        )

        self.review_1 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile_1,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Super helpful.",
        )
        self.review_3 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile_3,
            lecturer=self.lecturer_profile,
            rating=4,
            review="Great lesson.",
        )
        self.review_4 = create_review(
            lesson=self.course.lessons.all()[1],
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=2,
            review="Terrible.",
        )
        self.review_5 = create_review(
            lesson=self.course.lessons.all()[1],
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
            "lesson": self.course.lessons.all()[0].id,
            "lecturer": self.lecturer_profile.id,
            "rating": 3,
            "review": "Good lesson.",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reviews_number(), 5)

    def test_create_review_authenticated_not_purchased(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course.lessons.all()[3].id,
            "lecturer": self.lecturer_profile.id,
            "rating": 3,
            "review": "Good lesson.",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reviews_number(), 5)

    def test_create_review_authenticated_already_created(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course.lessons.all()[0].id,
            "lecturer": self.lecturer_profile.id,
            "rating": 3,
            "review": "Good lesson.",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reviews_number(), 5)

    def test_create_review_authenticated_incorrect_rating(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course.lessons.all()[0].id,
            "lecturer": self.lecturer_profile.id,
            "rating": 3.4,
            "review": "Good lesson.",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reviews_number(), 5)

    def test_create_review_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course.lessons.all()[2].id,
            "lecturer": self.lecturer_profile.id,
            "rating": 3.5,
            "review": "Good lesson.",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reviews_number(), 6)

    def test_update_review_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course.lessons.all()[0].id,
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
            "lesson": self.course.lessons.all()[2].id,
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
            "lesson": self.course.lessons.all()[0].id,
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
        self.assertEqual(
            lecturer, get_profile(get_user(self.review_1.lecturer.user.email)).id
        )

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
        self.endpoint = "/best-reviews"
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
        self.profile_1 = create_profile(user=self.user_1)
        self.profile_2 = create_profile(user=self.user_2)
        self.profile_3 = create_profile(user=self.user_3)

        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_profile(user=self.lecturer_user, user_type="W")

        self.course = create_course(
            title="course_title",
            description="course_description",
            technology=[create_technology_obj(name="Python")],
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
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 3",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="2.99",
                ),
            ],
        )

        self.review_1 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile_1,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Super helpful.",
        )
        self.review_3 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile_3,
            lecturer=self.lecturer_profile,
            rating=4,
            review="Great lesson.",
        )
        self.review_4 = create_review(
            lesson=self.course.lessons.all()[1],
            student=self.profile_1,
            lecturer=self.lecturer_profile,
            rating=3,
        )
        self.review_5 = create_review(
            lesson=self.course.lessons.all()[1],
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=2,
            review="Terrible.",
        )
        self.review_6 = create_review(
            lesson=self.course.lessons.all()[1],
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
        self.endpoint = "/reviews-stats"
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
        self.profile_1 = create_profile(user=self.user_1)
        self.profile_2 = create_profile(user=self.user_2)
        self.profile_3 = create_profile(user=self.user_3)

        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_profile(user=self.lecturer_user, user_type="W")

        self.course = create_course(
            title="course_title",
            description="course_description",
            technology=[create_technology_obj(name="Python")],
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
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 3",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 4",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="2.99",
                ),
            ],
        )

        create_purchase(
            lesson=self.course.lessons.all()[0],
            student=self.profile_1,
            price=self.course.lessons.all()[0].price,
        )
        create_purchase(
            lesson=self.course.lessons.all()[1],
            student=self.profile_1,
            price=self.course.lessons.all()[1].price,
        )
        create_purchase(
            lesson=self.course.lessons.all()[2],
            student=self.profile_1,
            price=self.course.lessons.all()[2].price,
        )

        self.review_1 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile_1,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Super helpful.",
        )
        self.review_3 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile_3,
            lecturer=self.lecturer_profile,
            rating=4,
            review="Great lesson.",
        )
        self.review_4 = create_review(
            lesson=self.course.lessons.all()[1],
            student=self.profile_2,
            lecturer=self.lecturer_profile,
            rating=2,
            review="Terrible.",
        )
        self.review_5 = create_review(
            lesson=self.course.lessons.all()[1],
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

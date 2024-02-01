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
    create_teaching,
    create_schedule,
    create_course_price_history,
    create_lesson_price_history,
    create_reservation,
    create_technology,
)
from .helpers import login
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class CourseFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/courses"
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
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_profile(user=self.user_2)
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
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )
        # course 1
        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
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
            ],
        )

        create_teaching(
            lesson=self.course_1.lessons.all()[0],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course_1.lessons.all()[1],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course_1.lessons.all()[0],
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.course_1.lessons.all()[1],
            lecturer=self.lecturer_profile_2,
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

        self.review_course_1_1 = create_review(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.course_1.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        # course 2
        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            technology=[create_technology_obj(name="Javascript")],
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

        create_teaching(
            lesson=self.course_2.lessons.all()[0],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course_2.lessons.all()[1],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course_2.lessons.all()[2],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course_2.lessons.all()[0],
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.course_2.lessons.all()[1],
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.course_2.lessons.all()[2],
            lecturer=self.lecturer_profile_2,
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
        create_purchase(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile_2,
            price=self.course_2.lessons.all()[0].price,
        )
        create_purchase(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile_2,
            price=self.course_2.lessons.all()[1].price,
        )
        create_purchase(
            lesson=self.course_2.lessons.all()[2],
            student=self.profile_2,
            price=self.course_2.lessons.all()[2].price,
        )

        self.review_course_2_1 = create_review(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_2_2 = create_review(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_2_3 = create_review(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=2,
            review="So so lesson.",
        )
        self.review_course_2_4 = create_review(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=1,
            review="So so lesson.",
        )
        self.review_course_2_5 = create_review(
            lesson=self.course_2.lessons.all()[2],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="So so lesson.",
        )

        # course 3
        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            technology=[create_technology_obj(name="VBA")],
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

        create_teaching(
            lesson=self.course_3.lessons.all()[0],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course_3.lessons.all()[0],
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile,
            price=self.course_3.lessons.all()[0].price,
        )
        create_purchase(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile_2,
            price=self.course_3.lessons.all()[0].price,
        )

        self.review_course_3_1 = create_review(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_3_2 = create_review(
            lesson=self.course_3.lessons.all()[0],
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
            [str(self.lecturer_profile_1.uuid), str(self.lecturer_profile_2.uuid)]
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
        self.endpoint = "/reviews"
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
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_profile(user=self.user_2)
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
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )
        # course 1
        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
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
            ],
        )

        self.review_course_1_1 = create_review(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.course_1.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        # course 2
        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            technology=[create_technology_obj(name="Javascript")],
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

        self.review_course_2_1 = create_review(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_2_2 = create_review(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_2_3 = create_review(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=2,
            review="So so lesson.",
        )
        self.review_course_2_4 = create_review(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=1,
            review="So so lesson.",
        )
        self.review_course_2_5 = create_review(
            lesson=self.course_2.lessons.all()[2],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="So so lesson.",
        )

        # course 3
        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            technology=[create_technology_obj(name="VBA")],
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

        self.review_course_3_1 = create_review(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_3_2 = create_review(
            lesson=self.course_3.lessons.all()[0],
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
        response = self.client.get(
            f"{self.endpoint}?lesson_id={self.course_1.lessons.all()[0].id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_lecturer_id_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?lecturer_id={self.lecturer_profile_1.uuid}"
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
        self.endpoint = "/schedules"
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
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_profile(user=self.user_2)
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
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )
        # course 1
        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
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
            ],
        )

        for lesson in self.course_1.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile_1,
                lesson=lesson,
            )
            create_teaching(
                lecturer=self.lecturer_profile_2,
                lesson=lesson,
            )

        # course 2
        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            technology=[create_technology_obj(name="Javascript")],
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

        for lesson in self.course_2.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile_1,
                lesson=lesson,
            )
            create_teaching(
                lecturer=self.lecturer_profile_2,
                lesson=lesson,
            )

        # course 3
        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            technology=[create_technology_obj(name="VBA")],
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

        for lesson in self.course_3.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile_1,
                lesson=lesson,
            )
            create_teaching(
                lecturer=self.lecturer_profile_2,
                lesson=lesson,
            )

        self.schedules = []
        for i in range(10):
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile_1,
                    time=make_aware(
                        datetime.now().replace(minute=15, second=0, microsecond=0)
                        + timedelta(minutes=15 * i)
                    ),
                )
            )
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile_2,
                    time=make_aware(
                        datetime.now().replace(minute=15, second=0, microsecond=0)
                        + timedelta(minutes=15 * i)
                    ),
                )
            )

        create_reservation(
            student=self.profile,
            lesson=self.course_1.lessons.all()[0],
            schedule=self.schedules[0],
        )
        create_reservation(
            student=self.profile,
            lesson=self.course_1.lessons.all()[1],
            schedule=self.schedules[1],
        )

    def test_lesson_id_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?lesson_id={self.course_1.lessons.all()[0].id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 19)

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


class CoursePriceHistoryFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/course-price-history"
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
            ],
        )

        create_course_price_history(self.course, 80)
        create_course_price_history(self.course, 100)
        create_course_price_history(self.course, 120)
        create_lesson_price_history(self.course.lessons.all()[0], 15)
        create_lesson_price_history(self.course.lessons.all()[0], 25)
        create_lesson_price_history(self.course.lessons.all()[0], 5)
        create_lesson_price_history(self.course.lessons.all()[1], 1)
        create_lesson_price_history(self.course.lessons.all()[1], 5)
        create_lesson_price_history(self.course.lessons.all()[1], 3)

        self.course_2 = create_course(
            title="course_title 2",
            description="course_description",
            technology=[create_technology_obj(name="JS")],
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
            ],
        )

        create_course_price_history(self.course_2, 120)
        create_course_price_history(self.course_2, 100)
        create_course_price_history(self.course_2, 80)
        create_lesson_price_history(self.course_2.lessons.all()[0], 15)
        create_lesson_price_history(self.course_2.lessons.all()[0], 25)
        create_lesson_price_history(self.course_2.lessons.all()[0], 5)
        create_lesson_price_history(self.course_2.lessons.all()[1], 1)
        create_lesson_price_history(self.course_2.lessons.all()[1], 5)
        create_lesson_price_history(self.course_2.lessons.all()[1], 3)

        self.course_3 = create_course(
            title="course_title 3",
            description="course_description",
            technology=[create_technology_obj(name="VBA")],
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
                    title="VBA lesson 1",
                    description="bbbb",
                    duration="90",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="VBA lesson 2",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="2.99",
                ),
            ],
        )

        create_course_price_history(self.course_3, 100)
        create_course_price_history(self.course_3, 80)
        create_course_price_history(self.course_3, 120)
        create_lesson_price_history(self.course_3.lessons.all()[0], 15)
        create_lesson_price_history(self.course_3.lessons.all()[0], 25)
        create_lesson_price_history(self.course_3.lessons.all()[0], 5)
        create_lesson_price_history(self.course_3.lessons.all()[1], 1)
        create_lesson_price_history(self.course_3.lessons.all()[1], 5)
        create_lesson_price_history(self.course_3.lessons.all()[1], 3)

    def test_course_id_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?course_id={self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        prices = [record["price"] for record in results]
        self.assertEqual(prices, ["80.00", "100.00", "120.00"])


class LessonPriceHistoryFilterTest(APITestCase):
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
            ],
        )

        create_course_price_history(self.course, 80)
        create_course_price_history(self.course, 100)
        create_course_price_history(self.course, 120)
        create_lesson_price_history(self.course.lessons.all()[0], 15)
        create_lesson_price_history(self.course.lessons.all()[0], 25)
        create_lesson_price_history(self.course.lessons.all()[0], 5)
        create_lesson_price_history(self.course.lessons.all()[1], 1)
        create_lesson_price_history(self.course.lessons.all()[1], 5)
        create_lesson_price_history(self.course.lessons.all()[1], 3)

        self.course_2 = create_course(
            title="course_title 2",
            description="course_description",
            technology=[create_technology_obj(name="JS")],
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
            ],
        )

        create_course_price_history(self.course_2, 120)
        create_course_price_history(self.course_2, 100)
        create_course_price_history(self.course_2, 80)
        create_lesson_price_history(self.course_2.lessons.all()[0], 15)
        create_lesson_price_history(self.course_2.lessons.all()[0], 25)
        create_lesson_price_history(self.course_2.lessons.all()[0], 5)
        create_lesson_price_history(self.course_2.lessons.all()[1], 1)
        create_lesson_price_history(self.course_2.lessons.all()[1], 5)
        create_lesson_price_history(self.course_2.lessons.all()[1], 3)

        self.course_3 = create_course(
            title="course_title 3",
            description="course_description",
            technology=[create_technology_obj(name="VBA")],
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
                    title="VBA lesson 1",
                    description="bbbb",
                    duration="90",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="VBA lesson 2",
                    description="bbbb",
                    duration="30",
                    github_url="https://github.com/hackymatt/course/lesson",
                    price="2.99",
                ),
            ],
        )

        create_course_price_history(self.course_3, 100)
        create_course_price_history(self.course_3, 80)
        create_course_price_history(self.course_3, 120)
        create_lesson_price_history(self.course_3.lessons.all()[0], 15)
        create_lesson_price_history(self.course_3.lessons.all()[0], 25)
        create_lesson_price_history(self.course_3.lessons.all()[0], 5)
        create_lesson_price_history(self.course_3.lessons.all()[1], 1)
        create_lesson_price_history(self.course_3.lessons.all()[1], 5)
        create_lesson_price_history(self.course_3.lessons.all()[1], 3)

    def test_lesson_id_filter(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?lesson_id={self.course.lessons.all()[0].id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        prices = [record["price"] for record in results]
        self.assertEqual(prices, ["15.00", "25.00", "5.00"])


class TechnologyFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/technologies"
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


class LecturerFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/lecturers"
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
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_profile(user=self.user_2)
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
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )
        # course 1
        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
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
            ],
        )

        create_teaching(
            lesson=self.course_1.lessons.all()[0],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course_1.lessons.all()[1],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course_1.lessons.all()[0],
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.course_1.lessons.all()[1],
            lecturer=self.lecturer_profile_2,
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

        self.review_course_1_1 = create_review(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.course_1.lessons.all()[1],
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

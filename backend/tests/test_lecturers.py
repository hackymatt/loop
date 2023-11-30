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
    create_review,
)
from .helpers import login
from django.contrib import auth
import json


class LecturersTest(APITestCase):
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
        self.student_profile_1 = create_profile(user=self.student_user_1)
        self.student_profile_2 = create_profile(user=self.student_user_2)
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )

        # course 1
        self.course = create_course(
            title="Python Beginner",
            description="Learn Python today",
            technology=create_technology_obj(name="Python"),
            level="Podstawowy",
            price="99.99",
            github_repo_link="www.example.com",
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
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
            ],
        )

        create_teaching(
            lesson=self.course.lessons.all()[0],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course.lessons.all()[1],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course.lessons.all()[0],
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.course.lessons.all()[1],
            lecturer=self.lecturer_profile_2,
        )

        self.review_course_1_1 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.student_profile_1,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.student_profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.course.lessons.all()[1],
            student=self.student_profile_1,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

    def test_get_lecturers_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_get_lecturers_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)


class BestLecturersTest(APITestCase):
    def setUp(self):
        self.endpoint = "/best-lecturers"
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
        self.student_profile_1 = create_profile(user=self.student_user_1)
        self.student_profile_2 = create_profile(user=self.student_user_2)
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )

        # course 1
        self.course = create_course(
            title="Python Beginner",
            description="Learn Python today",
            technology=create_technology_obj(name="Python"),
            level="Podstawowy",
            price="99.99",
            github_repo_link="www.example.com",
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
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
            ],
        )

        create_teaching(
            lesson=self.course.lessons.all()[0],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course.lessons.all()[1],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course.lessons.all()[0],
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.course.lessons.all()[1],
            lecturer=self.lecturer_profile_2,
        )

        self.review_course_1_1 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.student_profile_1,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.student_profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.course.lessons.all()[1],
            student=self.student_profile_1,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="So so lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.course.lessons.all()[1],
            student=self.student_profile_1,
            lecturer=self.lecturer_profile_2,
            rating=3,
            review="So so lesson.",
        )

    def test_get_best_lecturers_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 1)

    def test_get_best_lecturers_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 1)

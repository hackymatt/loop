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
    create_course_price_history,
    create_lesson_price_history,
)
from .helpers import (
    login,
    is_data_match,
    get_user,
    get_profile,
    get_lesson,
    filter_dict,
)
from django.contrib import auth
import json


class LessonTest(APITestCase):
    def setUp(self):
        self.endpoint = "/lessons"
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

        create_purchase(
            lesson=self.course.lessons.all()[0],
            student=self.profile,
            price=self.course.lessons.all()[0].price,
        )
        create_purchase(
            lesson=self.course.lessons.all()[1],
            student=self.profile,
            price=self.course.lessons.all()[1].price,
        )

        self.review_1 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_3 = create_review(
            lesson=self.course.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

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

        create_teaching(
            lesson=self.course_2.lessons.all()[0],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course_2.lessons.all()[1],
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

        self.review_4 = create_review(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_5 = create_review(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

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

        create_teaching(
            lesson=self.course_3.lessons.all()[0],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course_3.lessons.all()[1],
            lecturer=self.lecturer_profile_1,
        )
        create_teaching(
            lesson=self.course_3.lessons.all()[0],
            lecturer=self.lecturer_profile_2,
        )
        create_teaching(
            lesson=self.course_3.lessons.all()[1],
            lecturer=self.lecturer_profile_2,
        )

        create_purchase(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile,
            price=self.course_3.lessons.all()[0].price,
        )
        create_purchase(
            lesson=self.course_3.lessons.all()[1],
            student=self.profile,
            price=self.course_3.lessons.all()[1].price,
        )

        self.review_6 = create_review(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_7 = create_review(
            lesson=self.course_3.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        self.user_columns = ["first_name", "last_name", "email"]
        self.profile_columns = ["uuid"]

    def test_get_lessons_no_admin(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_lessons_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        results = data["results"]
        self.assertEqual(count, 6)
        for lesson_data in results:
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            if lesson_data["id"] == self.review_1.lesson.id:
                self.assertEqual(rating, 4.5)
                self.assertEqual(rating_count, 2)
                self.assertEqual(students_count, 1)
            elif (
                lesson_data["id"] == self.review_2.lesson.id
                or lesson_data["id"] == self.review_3.lesson.id
                or lesson_data["id"] == self.review_5.lesson.id
                or lesson_data["id"] == self.review_7.lesson.id
            ):
                self.assertEqual(rating, 3.0)
                self.assertEqual(rating_count, 1)
                self.assertEqual(students_count, 1)
            elif (
                lesson_data["id"] == self.review_4.lesson.id
                or lesson_data["id"] == self.review_6.lesson.id
            ):
                self.assertEqual(rating, 4.0)
                self.assertEqual(rating_count, 1)
                self.assertEqual(students_count, 1)

            for lecturer_data in lecturers_data:
                user_data = filter_dict(lecturer_data, self.user_columns)
                profile_data = filter_dict(lecturer_data, self.profile_columns)
                self.assertTrue(
                    is_data_match(get_user(lecturer_data["email"]), user_data)
                )
                self.assertTrue(
                    is_data_match(
                        get_profile(get_user(lecturer_data["email"])), profile_data
                    )
                )

    def test_get_lesson_unauthorized(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.course.lessons.all()[0].id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        lecturers_data = data.pop("lecturers")
        rating = data.pop("rating")
        rating_count = data.pop("rating_count")
        students_count = data.pop("students_count")

        self.assertTrue(is_data_match(get_lesson(data["id"]), data))
        self.assertEqual(rating, 4.5)
        self.assertEqual(rating_count, 2)
        self.assertEqual(students_count, 1)

        for lecturer_data in lecturers_data:
            user_data = filter_dict(lecturer_data, self.user_columns)
            profile_data = filter_dict(lecturer_data, self.profile_columns)
            self.assertTrue(is_data_match(get_user(lecturer_data["email"]), user_data))
            self.assertTrue(
                is_data_match(
                    get_profile(get_user(lecturer_data["email"])), profile_data
                )
            )

    def test_get_lesson_authorized(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.course.lessons.all()[0].id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)

        lecturers_data = data.pop("lecturers")
        rating = data.pop("rating")
        rating_count = data.pop("rating_count")
        students_count = data.pop("students_count")

        self.assertTrue(is_data_match(get_lesson(data["id"]), data))
        self.assertEqual(rating, 4.5)
        self.assertEqual(rating_count, 2)
        self.assertEqual(students_count, 1)

        for lecturer_data in lecturers_data:
            user_data = filter_dict(lecturer_data, self.user_columns)
            profile_data = filter_dict(lecturer_data, self.profile_columns)
            self.assertTrue(is_data_match(get_user(lecturer_data["email"]), user_data))
            self.assertTrue(
                is_data_match(
                    get_profile(get_user(lecturer_data["email"])), profile_data
                )
            )

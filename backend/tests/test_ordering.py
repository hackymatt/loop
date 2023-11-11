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
    create_lecturer_obj,
    create_review,
    create_purchase,
)
from django.contrib import auth
import json


def is_float(element: any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


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
            title="Python Begginer",
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
                    lecturers=[
                        create_lecturer_obj(self.lecturer_profile_1),
                        create_lecturer_obj(self.lecturer_profile_2),
                    ],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        )

        create_purchase(lesson=self.course_1.lessons.all()[0], profile=self.profile)
        create_purchase(lesson=self.course_1.lessons.all()[1], profile=self.profile)

        self.review_course_1_1 = create_review(
            lesson=self.course_1.lessons.all()[0],
            profile=self.profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.course_1.lessons.all()[0],
            profile=self.profile_2,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.course_1.lessons.all()[1],
            profile=self.profile,
            rating=3,
            review="So so lesson.",
        )

        # course 2
        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            technology=create_technology_obj(name="Javascript"),
            level="Zaawansowany",
            price="300",
            github_repo_link="www.example.com",
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
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer_obj(self.lecturer_profile_1),
                        create_lecturer_obj(self.lecturer_profile_2),
                    ],
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 3",
                    description="bbbb",
                    duration="130",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        )

        create_purchase(lesson=self.course_2.lessons.all()[0], profile=self.profile)
        create_purchase(lesson=self.course_2.lessons.all()[1], profile=self.profile)
        create_purchase(lesson=self.course_2.lessons.all()[0], profile=self.profile_2)
        create_purchase(lesson=self.course_2.lessons.all()[1], profile=self.profile_2)
        create_purchase(lesson=self.course_2.lessons.all()[2], profile=self.profile_2)

        self.review_course_2_1 = create_review(
            lesson=self.course_2.lessons.all()[0],
            profile=self.profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_2_2 = create_review(
            lesson=self.course_2.lessons.all()[1],
            profile=self.profile,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_2_3 = create_review(
            lesson=self.course_2.lessons.all()[0],
            profile=self.profile_2,
            rating=2,
            review="So so lesson.",
        )
        self.review_course_2_4 = create_review(
            lesson=self.course_2.lessons.all()[1],
            profile=self.profile_2,
            rating=1,
            review="So so lesson.",
        )
        self.review_course_2_5 = create_review(
            lesson=self.course_2.lessons.all()[2],
            profile=self.profile_2,
            rating=4,
            review="So so lesson.",
        )

        # course 3
        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            technology=create_technology_obj(name="VBA"),
            level="Ekspert",
            price="220",
            github_repo_link="www.example.com",
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
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer_obj(self.lecturer_profile_1),
                        create_lecturer_obj(self.lecturer_profile_2),
                    ],
                ),
            ],
        )

        create_purchase(lesson=self.course_3.lessons.all()[0], profile=self.profile)
        create_purchase(lesson=self.course_3.lessons.all()[0], profile=self.profile_2)

        self.review_course_3_1 = create_review(
            lesson=self.course_3.lessons.all()[0],
            profile=self.profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_3_2 = create_review(
            lesson=self.course_3.lessons.all()[0],
            profile=self.profile_2,
            rating=2,
            review="So so lesson.",
        )

        self.fields = ["title", "technology", "level", "price", "duration", "rating"]

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
            title="Python Begginer",
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
                    lecturers=[
                        create_lecturer_obj(self.lecturer_profile_1),
                        create_lecturer_obj(self.lecturer_profile_2),
                    ],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        )

        create_purchase(lesson=self.course_1.lessons.all()[0], profile=self.profile)
        create_purchase(lesson=self.course_1.lessons.all()[1], profile=self.profile)

        self.review_course_1_1 = create_review(
            lesson=self.course_1.lessons.all()[0],
            profile=self.profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.course_1.lessons.all()[0],
            profile=self.profile_2,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.course_1.lessons.all()[1],
            profile=self.profile,
            rating=3,
            review="So so lesson.",
        )

        # course 2
        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            technology=create_technology_obj(name="Javascript"),
            level="Zaawansowany",
            price="300",
            github_repo_link="www.example.com",
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
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer_obj(self.lecturer_profile_1),
                        create_lecturer_obj(self.lecturer_profile_2),
                    ],
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 3",
                    description="bbbb",
                    duration="130",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        )

        create_purchase(lesson=self.course_2.lessons.all()[0], profile=self.profile)
        create_purchase(lesson=self.course_2.lessons.all()[1], profile=self.profile)
        create_purchase(lesson=self.course_2.lessons.all()[0], profile=self.profile_2)
        create_purchase(lesson=self.course_2.lessons.all()[1], profile=self.profile_2)
        create_purchase(lesson=self.course_2.lessons.all()[2], profile=self.profile_2)

        self.review_course_2_1 = create_review(
            lesson=self.course_2.lessons.all()[0],
            profile=self.profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_2_2 = create_review(
            lesson=self.course_2.lessons.all()[1],
            profile=self.profile,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_2_3 = create_review(
            lesson=self.course_2.lessons.all()[0],
            profile=self.profile_2,
            rating=2,
            review="So so lesson.",
        )
        self.review_course_2_4 = create_review(
            lesson=self.course_2.lessons.all()[1],
            profile=self.profile_2,
            rating=1,
            review="So so lesson.",
        )
        self.review_course_2_5 = create_review(
            lesson=self.course_2.lessons.all()[2],
            profile=self.profile_2,
            rating=4,
            review="So so lesson.",
        )

        # course 3
        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            technology=create_technology_obj(name="VBA"),
            level="Ekspert",
            price="220",
            github_repo_link="www.example.com",
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
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer_obj(self.lecturer_profile_1),
                        create_lecturer_obj(self.lecturer_profile_2),
                    ],
                ),
            ],
        )

        create_purchase(lesson=self.course_3.lessons.all()[0], profile=self.profile)
        create_purchase(lesson=self.course_3.lessons.all()[0], profile=self.profile_2)

        self.review_course_3_1 = create_review(
            lesson=self.course_3.lessons.all()[0],
            profile=self.profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_3_2 = create_review(
            lesson=self.course_3.lessons.all()[0],
            profile=self.profile_2,
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

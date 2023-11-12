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
from .helpers import (
    login,
    is_data_match,
    get_user,
    get_profile,
    get_course,
    get_lesson,
    get_technology,
    get_skill,
    get_topic,
    courses_number,
    is_course_found,
    filter_dict,
    lessons_number,
)
from django.contrib import auth
import json


class CourseTest(APITestCase):
    def setUp(self):
        self.endpoint = "/courses"
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

        create_purchase(lesson=self.course.lessons.all()[0], student=self.profile)
        create_purchase(lesson=self.course.lessons.all()[1], student=self.profile)

        self.review_1 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile,
            rating=5,
            review="Great lesson.",
        )
        self.review_2 = create_review(
            lesson=self.course.lessons.all()[0],
            student=self.profile_2,
            rating=4,
            review="Good lesson.",
        )
        self.review_3 = create_review(
            lesson=self.course.lessons.all()[1],
            student=self.profile,
            rating=3,
            review="So so lesson.",
        )

        self.user_columns = ["first_name", "last_name", "email"]
        self.profile_columns = ["uuid"]

    def test_get_courses_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        results = data["results"]
        self.assertFalse(all("lessons" in course.keys() for course in results))
        self.assertFalse(all("skills" in course.keys() for course in results))
        self.assertFalse(all("topics" in course.keys() for course in results))
        self.assertEqual(results[0]["rating"], 4.0)
        self.assertEqual(results[0]["rating_count"], 3)
        self.assertEqual(results[0]["students_count"], 2)

    def test_get_courses_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        results = data["results"]
        self.assertFalse(all("lessons" in course.keys() for course in results))
        self.assertFalse(all("skills" in course.keys() for course in results))
        self.assertFalse(all("topics" in course.keys() for course in results))
        self.assertEqual(results[0]["rating"], 4.0)
        self.assertEqual(results[0]["rating_count"], 3)
        self.assertEqual(results[0]["students_count"], 2)

    def test_get_course_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course_data = json.loads(response.content)
        lessons_data = course_data.pop("lessons")
        technology_data = course_data.pop("technology")
        skills_data = course_data.pop("skills")
        topics_data = course_data.pop("topics")
        duration = course_data.pop("duration")
        lecturers = course_data.pop("lecturers")
        rating = course_data.pop("rating")
        rating_count = course_data.pop("rating_count")
        students_count = course_data.pop("students_count")
        self.assertTrue(is_data_match(get_course(self.course.id), course_data))
        self.assertTrue(
            is_data_match(get_technology(technology_data["id"]), technology_data)
        )
        self.assertEqual(
            duration, sum(lesson_data["duration"] for lesson_data in lessons_data)
        )
        self.assertEqual(
            lecturers,
            [
                dict(y)
                for y in set(
                    tuple(x.items())
                    for x in sum([lesson["lecturers"] for lesson in lessons_data], [])
                )
            ],
        )
        self.assertEqual(rating, 4.0)
        self.assertEqual(rating_count, 3)
        self.assertEqual(students_count, 2)
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            if lesson_data["id"] == self.review_1.lesson.id:
                self.assertEqual(rating, 4.5)
                self.assertEqual(rating_count, 2)
                self.assertEqual(students_count, 1)
            elif lesson_data["id"] == self.review_3.lesson.id:
                self.assertEqual(rating, 3.0)
                self.assertEqual(rating_count, 1)
                self.assertEqual(students_count, 1)
            else:
                self.assertEqual(rating, None)
                self.assertEqual(rating_count, 0)
                self.assertEqual(students_count, 2)
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
        for skill_data in skills_data:
            self.assertTrue(is_data_match(get_skill(skill_data["id"]), skill_data))
        for topic_data in topics_data:
            self.assertTrue(is_data_match(get_topic(topic_data["id"]), topic_data))

    def test_get_course_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course_data = json.loads(response.content)
        lessons_data = course_data.pop("lessons")
        technology_data = course_data.pop("technology")
        skills_data = course_data.pop("skills")
        topics_data = course_data.pop("topics")
        duration = course_data.pop("duration")
        lecturers = course_data.pop("lecturers")
        rating = course_data.pop("rating")
        rating_count = course_data.pop("rating_count")
        students_count = course_data.pop("students_count")
        self.assertTrue(is_data_match(get_course(self.course.id), course_data))
        self.assertTrue(
            is_data_match(get_technology(technology_data["id"]), technology_data)
        )
        self.assertEqual(
            duration, sum(lesson_data["duration"] for lesson_data in lessons_data)
        )
        self.assertEqual(
            lecturers,
            [
                dict(y)
                for y in set(
                    tuple(x.items())
                    for x in sum([lesson["lecturers"] for lesson in lessons_data], [])
                )
            ],
        )
        self.assertEqual(rating, 4.0)
        self.assertEqual(rating_count, 3)
        self.assertEqual(students_count, 2)
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            if lesson_data["id"] == self.review_1.lesson.id:
                self.assertEqual(rating, 4.5)
                self.assertEqual(rating_count, 2)
                self.assertEqual(students_count, 1)
            elif lesson_data["id"] == self.review_3.lesson.id:
                self.assertEqual(rating, 3.0)
                self.assertEqual(rating_count, 1)
                self.assertEqual(students_count, 1)
            else:
                self.assertEqual(rating, None)
                self.assertEqual(rating_count, 0)
                self.assertEqual(students_count, 0)
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
        for skill_data in skills_data:
            self.assertTrue(is_data_match(get_skill(skill_data["id"]), skill_data))
        for topic_data in topics_data:
            self.assertTrue(is_data_match(get_topic(topic_data["id"]), topic_data))

    def test_create_course_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "lessons": [
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 1",
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
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_1)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 1)

    def test_create_course_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "lessons": [
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 1",
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
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_1)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 1)

    def test_create_course_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            "topics": [
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            "lessons": [
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 1",
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
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_1)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        }

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(courses_number(), 2)
        course_data = json.loads(response.content)
        lessons_data = course_data.pop("lessons")
        technology_data = course_data.pop("technology")
        skills_data = course_data.pop("skills")
        topics_data = course_data.pop("topics")
        duration = course_data.pop("duration")
        lecturers = course_data.pop("lecturers")
        rating = course_data.pop("rating")
        rating_count = course_data.pop("rating_count")
        students_count = course_data.pop("students_count")
        self.assertTrue(is_data_match(get_course(course_data["id"]), course_data))
        self.assertTrue(
            is_data_match(get_technology(technology_data["id"]), technology_data)
        )
        self.assertEqual(
            duration, sum(lesson_data["duration"] for lesson_data in lessons_data)
        )
        self.assertEqual(
            lecturers,
            [
                dict(y)
                for y in set(
                    tuple(x.items())
                    for x in sum([lesson["lecturers"] for lesson in lessons_data], [])
                )
            ],
        )
        self.assertEqual(rating, None)
        self.assertEqual(rating_count, 0)
        self.assertEqual(students_count, 0)
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            self.assertEqual(rating, None)
            self.assertEqual(rating_count, 0)
            self.assertEqual(students_count, 0)
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
        for skill_data in skills_data:
            self.assertTrue(is_data_match(get_skill(skill_data["id"]), skill_data))
        for topic_data in topics_data:
            self.assertTrue(is_data_match(get_topic(topic_data["id"]), topic_data))

    def test_create_course_without_lesson(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            "topics": [
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            "lessons": [],
        }

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)

    def test_create_course_without_skills(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [],
            "topics": [
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            "lessons": [
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 1",
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
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_1)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        }

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)

    def test_create_course_without_topics(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            "topics": [],
            "lessons": [
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 1",
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
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_1)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        }

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)

    def test_update_course_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "lessons": [
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 1",
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
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_1)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        }
        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 1)

    def test_update_course_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "lessons": [
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 1",
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
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_1)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        }
        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 1)

    def test_update_course_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "active": "False",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            "topics": [
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            "lessons": [
                create_lesson_obj(
                    id=self.course.lessons.all()[0].id,
                    title="Javascript lesson 1",
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
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_1)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        }

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(courses_number(), 1)
        course_data = json.loads(response.content)
        lessons_data = course_data.pop("lessons")
        technology_data = course_data.pop("technology")
        skills_data = course_data.pop("skills")
        topics_data = course_data.pop("topics")
        duration = course_data.pop("duration")
        lecturers = course_data.pop("lecturers")
        rating = course_data.pop("rating")
        rating_count = course_data.pop("rating_count")
        students_count = course_data.pop("students_count")
        self.assertTrue(is_data_match(get_course(self.course.id), course_data))
        self.assertTrue(
            is_data_match(get_technology(technology_data["id"]), technology_data)
        )
        self.assertEqual(
            duration, sum(lesson_data["duration"] for lesson_data in lessons_data)
        )
        self.assertEqual(
            lecturers,
            [
                dict(y)
                for y in set(
                    tuple(x.items())
                    for x in sum([lesson["lecturers"] for lesson in lessons_data], [])
                )
            ],
        )
        self.assertEqual(rating, 4.5)
        self.assertEqual(rating_count, 2)
        self.assertEqual(students_count, 1)
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            if lesson_data["id"] == self.review_1.lesson.id:
                self.assertEqual(rating, 4.5)
                self.assertEqual(rating_count, 2)
                self.assertEqual(students_count, 1)
            else:
                self.assertEqual(rating, None)
                self.assertEqual(rating_count, 0)
                self.assertEqual(students_count, 0)
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
        for skill_data in skills_data:
            self.assertTrue(is_data_match(get_skill(skill_data["id"]), skill_data))
        for topic_data in topics_data:
            self.assertTrue(is_data_match(get_topic(topic_data["id"]), topic_data))

    def test_update_course_without_lesson(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            "topics": [
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            "lessons": [],
        }

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)

    def test_update_course_without_skills(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [],
            "topics": [
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            "lessons": [
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 1",
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
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_1)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        }

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)

    def test_update_course_without_topics(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            "topics": [],
            "lessons": [
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 1",
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
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_1)],
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer_obj(self.lecturer_profile_2)],
                ),
            ],
        }

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)

    def test_delete_course_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        response = self.client.delete(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 1)
        self.assertTrue(is_course_found(self.course.id))

    def test_delete_course_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        response = self.client.delete(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 1)
        self.assertTrue(is_course_found(self.course.id))

    def test_delete_course_authenticated_active(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        response = self.client.delete(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)
        self.assertTrue(is_course_found(self.course.id))

    def test_delete_course_authenticated_inactive(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.course.active = False
        self.course.save()
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        response = self.client.delete(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(courses_number(), 0)
        self.assertFalse(is_course_found(self.course.id))
        self.assertEqual(lessons_number(), 0)

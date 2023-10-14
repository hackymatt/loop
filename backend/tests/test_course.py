from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_course,
    create_lesson,
    create_technology,
    create_skill,
    create_topic,
    create_lecturer,
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
    filter_dict,
    lessons_number,
)
from django.contrib import auth
import json


class CourseTest(APITestCase):
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
            technology=create_technology(name="Python"),
            level="Podstawowy",
            price="99.99",
            github_repo_link="www.example.com",
            skills=[create_skill(name="coding"), create_skill(name="IDE")],
            topics=[
                create_topic(name="You will learn how to code"),
                create_topic(name="You will learn a new IDE"),
            ],
            lessons=[
                create_lesson(
                    title="Python lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer(self.lecturer_profile_1),
                        create_lecturer(self.lecturer_profile_2),
                    ],
                ),
                create_lesson(
                    title="Python lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer(self.lecturer_profile_2)],
                ),
            ],
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
        self.assertFalse(all("lessons" in course.keys() for course in data))
        self.assertFalse(all("skills" in course.keys() for course in data))
        self.assertFalse(all("topics" in course.keys() for course in data))

    def test_get_courses_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertFalse(all("lessons" in course.keys() for course in data))
        self.assertFalse(all("skills" in course.keys() for course in data))
        self.assertFalse(all("topics" in course.keys() for course in data))

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
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
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
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
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
            "technology": create_technology(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "lessons": [
                create_lesson(
                    title="Javascript lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer(self.lecturer_profile_1),
                        create_lecturer(self.lecturer_profile_2),
                    ],
                ),
                create_lesson(
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer(self.lecturer_profile_1)],
                ),
                create_lesson(
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer(self.lecturer_profile_2)],
                ),
            ],
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 1)

    def test_create_course_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill(name="coding"), create_skill(name="IDE")],
            "topics": [
                create_topic(name="You will learn how to code"),
                create_topic(name="You will learn a new IDE"),
            ],
            "lessons": [
                create_lesson(
                    title="Javascript lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer(self.lecturer_profile_1),
                        create_lecturer(self.lecturer_profile_2),
                    ],
                ),
                create_lesson(
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer(self.lecturer_profile_1)],
                ),
                create_lesson(
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer(self.lecturer_profile_2)],
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
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
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
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill(name="coding"), create_skill(name="IDE")],
            "topics": [
                create_topic(name="You will learn how to code"),
                create_topic(name="You will learn a new IDE"),
            ],
            "lessons": [],
        }

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)

    def test_create_course_without_skills(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [],
            "topics": [
                create_topic(name="You will learn how to code"),
                create_topic(name="You will learn a new IDE"),
            ],
            "lessons": [
                create_lesson(
                    title="Javascript lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer(self.lecturer_profile_1),
                        create_lecturer(self.lecturer_profile_2),
                    ],
                ),
                create_lesson(
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer(self.lecturer_profile_1)],
                ),
                create_lesson(
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer(self.lecturer_profile_2)],
                ),
            ],
        }

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)

    def test_create_course_without_topics(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill(name="coding"), create_skill(name="IDE")],
            "topics": [],
            "lessons": [
                create_lesson(
                    title="Javascript lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer(self.lecturer_profile_1),
                        create_lecturer(self.lecturer_profile_2),
                    ],
                ),
                create_lesson(
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer(self.lecturer_profile_1)],
                ),
                create_lesson(
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer(self.lecturer_profile_2)],
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
            "technology": create_technology(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "lessons": [
                create_lesson(
                    title="Javascript lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer(self.lecturer_profile_1),
                        create_lecturer(self.lecturer_profile_2),
                    ],
                ),
                create_lesson(
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer(self.lecturer_profile_1)],
                ),
                create_lesson(
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer(self.lecturer_profile_2)],
                ),
            ],
        }
        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 1)

    def test_update_course_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "active": "False",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill(name="coding"), create_skill(name="IDE")],
            "topics": [
                create_topic(name="You will learn how to code"),
                create_topic(name="You will learn a new IDE"),
            ],
            "lessons": [
                create_lesson(
                    title="Javascript lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer(self.lecturer_profile_1),
                        create_lecturer(self.lecturer_profile_2),
                    ],
                ),
                create_lesson(
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer(self.lecturer_profile_1)],
                ),
                create_lesson(
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer(self.lecturer_profile_2)],
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
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
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
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill(name="coding"), create_skill(name="IDE")],
            "topics": [
                create_topic(name="You will learn how to code"),
                create_topic(name="You will learn a new IDE"),
            ],
            "lessons": [],
        }

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)

    def test_update_course_without_skills(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [],
            "topics": [
                create_topic(name="You will learn how to code"),
                create_topic(name="You will learn a new IDE"),
            ],
            "lessons": [
                create_lesson(
                    title="Javascript lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer(self.lecturer_profile_1),
                        create_lecturer(self.lecturer_profile_2),
                    ],
                ),
                create_lesson(
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer(self.lecturer_profile_1)],
                ),
                create_lesson(
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer(self.lecturer_profile_2)],
                ),
            ],
        }

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)

    def test_update_course_without_topics(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology(name="Javascript"),
            "level": "E",
            "price": "999.99",
            "github_repo_link": "https://github.com/hackymatt/CodeEdu",
            "skills": [create_skill(name="coding"), create_skill(name="IDE")],
            "topics": [],
            "lessons": [
                create_lesson(
                    title="Javascript lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                    lecturers=[
                        create_lecturer(self.lecturer_profile_1),
                        create_lecturer(self.lecturer_profile_2),
                    ],
                ),
                create_lesson(
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                    lecturers=[create_lecturer(self.lecturer_profile_1)],
                ),
                create_lesson(
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="50",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                    lecturers=[create_lecturer(self.lecturer_profile_2)],
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

    def test_delete_course_authenticated_active(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        response = self.client.delete(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 1)

    def test_delete_course_authenticated_inactive(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.course.active = False
        self.course.save()
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        response = self.client.delete(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(courses_number(), 0)
        self.assertEqual(lessons_number(), 0)

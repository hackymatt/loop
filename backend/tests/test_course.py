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
    create_image,
    create_video,
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
)
from django.contrib import auth
import json
from base64 import b64encode


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
            technology=create_technology_obj(name="JS"),
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
                    title="JS lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
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
            technology=create_technology_obj(name="VBA"),
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
                    title="VBA lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="VBA lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
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
        self.assertEqual(results[0]["previous_price"], 120.0)
        self.assertEqual(results[0]["lowest_30_days_price"], 80.0)

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
        self.assertEqual(results[0]["previous_price"], 120.0)
        self.assertEqual(results[0]["lowest_30_days_price"], 80.0)

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
        previous_price = course_data.pop("previous_price")
        lowest_30_days_price = course_data.pop("lowest_30_days_price")
        self.assertTrue(is_data_match(get_course(self.course.id), course_data))
        self.assertTrue(
            is_data_match(get_technology(technology_data["id"]), technology_data)
        )
        self.assertEqual(
            duration, sum(lesson_data["duration"] for lesson_data in lessons_data)
        )
        self.assertEqual(
            lecturers,
            sorted(
                [
                    dict(y)
                    for y in set(
                        tuple(x.items())
                        for x in sum(
                            [lesson["lecturers"] for lesson in lessons_data], []
                        )
                    )
                ],
                key=lambda d: d["uuid"],
            ),
        )
        self.assertEqual(rating, 4.0)
        self.assertEqual(rating_count, 3)
        self.assertEqual(students_count, 2)
        self.assertEqual(previous_price, 120.0)
        self.assertEqual(lowest_30_days_price, 80.0)
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            previous_price = lesson_data.pop("previous_price")
            lowest_30_days_price = lesson_data.pop("lowest_30_days_price")
            is_bestseller = lesson_data.pop("is_bestseller")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            if lesson_data["id"] == self.review_1.lesson.id:
                self.assertEqual(rating, 4.5)
                self.assertEqual(rating_count, 2)
                self.assertEqual(students_count, 1)
                self.assertEqual(previous_price, None)
                self.assertEqual(lowest_30_days_price, None)
                self.assertEqual(is_bestseller, True)
            elif lesson_data["id"] == self.review_3.lesson.id:
                self.assertEqual(rating, 3.0)
                self.assertEqual(rating_count, 1)
                self.assertEqual(students_count, 1)
                self.assertEqual(previous_price, 3.0)
                self.assertEqual(lowest_30_days_price, 1.0)
                self.assertEqual(is_bestseller, False)
            else:
                self.assertEqual(rating, None)
                self.assertEqual(rating_count, 0)
                self.assertEqual(students_count, 0)
                self.assertEqual(previous_price, 1)
                self.assertEqual(lowest_30_days_price, 1)
                self.assertEqual(is_bestseller, False)
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
        previous_price = course_data.pop("previous_price")
        lowest_30_days_price = course_data.pop("lowest_30_days_price")
        self.assertTrue(is_data_match(get_course(self.course.id), course_data))
        self.assertTrue(
            is_data_match(get_technology(technology_data["id"]), technology_data)
        )
        self.assertEqual(
            duration, sum(lesson_data["duration"] for lesson_data in lessons_data)
        )
        self.assertEqual(
            lecturers,
            sorted(
                [
                    dict(y)
                    for y in set(
                        tuple(x.items())
                        for x in sum(
                            [lesson["lecturers"] for lesson in lessons_data], []
                        )
                    )
                ],
                key=lambda d: d["uuid"],
            ),
        )
        self.assertEqual(rating, 4.0)
        self.assertEqual(rating_count, 3)
        self.assertEqual(students_count, 2)
        self.assertEqual(previous_price, 120.0)
        self.assertEqual(lowest_30_days_price, 80.0)
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            previous_price = lesson_data.pop("previous_price")
            lowest_30_days_price = lesson_data.pop("lowest_30_days_price")
            is_bestseller = lesson_data.pop("is_bestseller")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            if lesson_data["id"] == self.review_1.lesson.id:
                self.assertEqual(rating, 4.5)
                self.assertEqual(rating_count, 2)
                self.assertEqual(students_count, 1)
                self.assertEqual(previous_price, None)
                self.assertEqual(lowest_30_days_price, None)
                self.assertEqual(is_bestseller, True)
            elif lesson_data["id"] == self.review_3.lesson.id:
                self.assertEqual(rating, 3.0)
                self.assertEqual(rating_count, 1)
                self.assertEqual(students_count, 1)
                self.assertEqual(previous_price, 3.0)
                self.assertEqual(lowest_30_days_price, 1.0)
                self.assertEqual(is_bestseller, False)
            else:
                self.assertEqual(rating, None)
                self.assertEqual(rating_count, 0)
                self.assertEqual(students_count, 0)
                self.assertEqual(previous_price, 2)
                self.assertEqual(lowest_30_days_price, 2)
                self.assertEqual(is_bestseller, False)
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
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 3)

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
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 3)

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
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
            "video": b64encode(create_video().read()),
        }

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(courses_number(), 4)
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
        previous_price = course_data.pop("previous_price")
        lowest_30_days_price = course_data.pop("lowest_30_days_price")
        self.assertTrue(is_data_match(get_course(course_data["id"]), course_data))
        self.assertTrue(
            is_data_match(get_technology(technology_data["id"]), technology_data)
        )
        self.assertEqual(
            duration, sum(lesson_data["duration"] for lesson_data in lessons_data)
        )
        self.assertEqual(
            lecturers,
            sorted(
                [
                    dict(y)
                    for y in set(
                        tuple(x.items())
                        for x in sum(
                            [lesson["lecturers"] for lesson in lessons_data], []
                        )
                    )
                ],
                key=lambda d: d["uuid"],
            ),
        )
        self.assertEqual(rating, None)
        self.assertEqual(rating_count, 0)
        self.assertEqual(students_count, 0)
        self.assertEqual(previous_price, None)
        self.assertEqual(lowest_30_days_price, None)
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            previous_price = lesson_data.pop("previous_price")
            lowest_30_days_price = lesson_data.pop("lowest_30_days_price")
            is_bestseller = lesson_data.pop("is_bestseller")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            self.assertEqual(rating, None)
            self.assertEqual(rating_count, 0)
            self.assertEqual(students_count, 0)
            self.assertEqual(previous_price, None)
            self.assertEqual(lowest_30_days_price, None)
            self.assertEqual(is_bestseller, False)
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
        self.assertEqual(courses_number(), 3)

    def test_create_course_lesson_incorrect_duration(self):
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
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="40",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)

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
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)

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
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)

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
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }
        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 3)

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
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }
        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 3)

    def test_update_course_authenticated_price_change_down(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "89.99",
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
                    price="8.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(courses_number(), 3)
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
        previous_price = course_data.pop("previous_price")
        lowest_30_days_price = course_data.pop("lowest_30_days_price")
        self.assertTrue(is_data_match(get_course(self.course.id), course_data))
        self.assertTrue(
            is_data_match(get_technology(technology_data["id"]), technology_data)
        )
        self.assertEqual(
            duration, sum(lesson_data["duration"] for lesson_data in lessons_data)
        )
        self.assertEqual(
            lecturers,
            sorted(
                [
                    dict(y)
                    for y in set(
                        tuple(x.items())
                        for x in sum(
                            [lesson["lecturers"] for lesson in lessons_data], []
                        )
                    )
                ],
                key=lambda d: d["uuid"],
            ),
        )
        self.assertEqual(rating, 4.5)
        self.assertEqual(rating_count, 2)
        self.assertEqual(students_count, 1)
        self.assertEqual(previous_price, 99.99)
        self.assertEqual(lowest_30_days_price, 80.0)
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            previous_price = lesson_data.pop("previous_price")
            lowest_30_days_price = lesson_data.pop("lowest_30_days_price")
            is_bestseller = lesson_data.pop("is_bestseller")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            if lesson_data["id"] == self.course.lessons.all()[0].id:
                self.assertEqual(rating, 4.5)
                self.assertEqual(rating_count, 2)
                self.assertEqual(students_count, 1)
                self.assertEqual(previous_price, 9.99)
                self.assertEqual(lowest_30_days_price, 5.0)
                self.assertEqual(is_bestseller, True)
            elif lesson_data["id"] == self.course.lessons.all()[1].id:
                self.assertEqual(rating, 3.0)
                self.assertEqual(rating_count, 1)
                self.assertEqual(students_count, 1)
                self.assertEqual(previous_price, 3.0)
                self.assertEqual(lowest_30_days_price, 1.0)
                self.assertEqual(is_bestseller, False)
            else:
                self.assertEqual(rating, None)
                self.assertEqual(rating_count, 0)
                self.assertEqual(students_count, 0)
                self.assertEqual(previous_price, None)
                self.assertEqual(lowest_30_days_price, None)
                self.assertEqual(is_bestseller, False)
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

    def test_update_course_authenticated_price_change_up(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "109.99",
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
                    price="8.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(courses_number(), 3)
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
        previous_price = course_data.pop("previous_price")
        lowest_30_days_price = course_data.pop("lowest_30_days_price")
        self.assertTrue(is_data_match(get_course(self.course.id), course_data))
        self.assertTrue(
            is_data_match(get_technology(technology_data["id"]), technology_data)
        )
        self.assertEqual(
            duration, sum(lesson_data["duration"] for lesson_data in lessons_data)
        )
        self.assertEqual(
            lecturers,
            sorted(
                [
                    dict(y)
                    for y in set(
                        tuple(x.items())
                        for x in sum(
                            [lesson["lecturers"] for lesson in lessons_data], []
                        )
                    )
                ],
                key=lambda d: d["uuid"],
            ),
        )
        self.assertEqual(rating, 4.5)
        self.assertEqual(rating_count, 2)
        self.assertEqual(students_count, 1)
        self.assertEqual(previous_price, None)
        self.assertEqual(lowest_30_days_price, None)

        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            previous_price = lesson_data.pop("previous_price")
            lowest_30_days_price = lesson_data.pop("lowest_30_days_price")
            is_bestseller = lesson_data.pop("is_bestseller")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            if lesson_data["id"] == self.course.lessons.all()[0].id:
                self.assertEqual(rating, 4.5)
                self.assertEqual(rating_count, 2)
                self.assertEqual(students_count, 1)
                self.assertEqual(previous_price, 9.99)
                self.assertEqual(lowest_30_days_price, 5.0)
                self.assertEqual(is_bestseller, True)
            elif lesson_data["id"] == self.course.lessons.all()[1].id:
                self.assertEqual(rating, 3.0)
                self.assertEqual(rating_count, 1)
                self.assertEqual(students_count, 1)
                self.assertEqual(previous_price, 3.0)
                self.assertEqual(lowest_30_days_price, 1.0)
                self.assertEqual(is_bestseller, False)
            else:
                self.assertEqual(rating, None)
                self.assertEqual(rating_count, 0)
                self.assertEqual(students_count, 0)
                self.assertEqual(previous_price, None)
                self.assertEqual(lowest_30_days_price, None)
                self.assertEqual(is_bestseller, False)
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

    def test_update_course_authenticated_no_price_change(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "title": "Javascript course",
            "description": "course_description",
            "technology": create_technology_obj(name="Javascript"),
            "level": "E",
            "price": "99.99",
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
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(courses_number(), 3)
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
        previous_price = course_data.pop("previous_price")
        lowest_30_days_price = course_data.pop("lowest_30_days_price")
        self.assertTrue(is_data_match(get_course(self.course.id), course_data))
        self.assertTrue(
            is_data_match(get_technology(technology_data["id"]), technology_data)
        )
        self.assertEqual(
            duration, sum(lesson_data["duration"] for lesson_data in lessons_data)
        )
        self.assertEqual(
            lecturers,
            sorted(
                [
                    dict(y)
                    for y in set(
                        tuple(x.items())
                        for x in sum(
                            [lesson["lecturers"] for lesson in lessons_data], []
                        )
                    )
                ],
                key=lambda d: d["uuid"],
            ),
        )
        self.assertEqual(rating, 4.5)
        self.assertEqual(rating_count, 2)
        self.assertEqual(students_count, 1)
        self.assertEqual(previous_price, 120.0)
        self.assertEqual(lowest_30_days_price, 80.0)
        for lesson_data in lessons_data:
            lecturers_data = lesson_data.pop("lecturers")
            rating = lesson_data.pop("rating")
            rating_count = lesson_data.pop("rating_count")
            students_count = lesson_data.pop("students_count")
            previous_price = lesson_data.pop("previous_price")
            lowest_30_days_price = lesson_data.pop("lowest_30_days_price")
            is_bestseller = lesson_data.pop("is_bestseller")
            self.assertTrue(is_data_match(get_lesson(lesson_data["id"]), lesson_data))
            if lesson_data["id"] == self.course.lessons.all()[0].id:
                self.assertEqual(rating, 4.5)
                self.assertEqual(rating_count, 2)
                self.assertEqual(students_count, 1)
                self.assertEqual(previous_price, None)
                self.assertEqual(lowest_30_days_price, None)
                self.assertEqual(is_bestseller, True)
            elif lesson_data["id"] == self.course.lessons.all()[1].id:
                self.assertEqual(rating, 3.0)
                self.assertEqual(rating_count, 1)
                self.assertEqual(students_count, 1)
                self.assertEqual(previous_price, 3.0)
                self.assertEqual(lowest_30_days_price, 1.0)
                self.assertEqual(is_bestseller, False)
            else:
                self.assertEqual(rating, None)
                self.assertEqual(rating_count, 0)
                self.assertEqual(students_count, 0)
                self.assertEqual(previous_price, None)
                self.assertEqual(lowest_30_days_price, None)
                self.assertEqual(is_bestseller, False)
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
        self.assertEqual(courses_number(), 3)

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
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)

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
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Javascript lesson 3",
                    description="bbbb",
                    duration="60",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="29.99",
                ),
            ],
            "image": b64encode(create_image().read()),
        }

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)


class BestCourseTest(APITestCase):
    def setUp(self):
        self.endpoint = "/best-courses"
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
            technology=create_technology_obj(name="JS"),
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
                    title="JS lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
            ],
        )

        self.course_3 = create_course(
            title="course_title 3",
            description="course_description",
            technology=create_technology_obj(name="VBA"),
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
                    title="VBA lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="VBA lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
            ],
        )

    def test_get_best_courses_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 1)

    def test_get_best_courses_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 1)


class CoursePriceHistoryTest(APITestCase):
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
            technology=create_technology_obj(name="JS"),
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
                    title="JS lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
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
            technology=create_technology_obj(name="VBA"),
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
                    title="VBA lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="VBA lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
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

    def test_get_course_price_history_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_price_history_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_price_history_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 9)
        prices = [record["price"] for record in results]
        self.assertEqual(
            prices,
            [
                "80.00",
                "100.00",
                "120.00",
                "120.00",
                "100.00",
                "80.00",
                "100.00",
                "80.00",
                "120.00",
            ],
        )


class LessonPriceHistoryTest(APITestCase):
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
            technology=create_technology_obj(name="JS"),
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
                    title="JS lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
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
            technology=create_technology_obj(name="VBA"),
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
                    title="VBA lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="VBA lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
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

    def test_get_lesson_price_history_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_lesson_price_history_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_lesson_price_history_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 18)
        prices = [record["price"] for record in results]
        self.assertEqual(
            prices,
            [
                "15.00",
                "25.00",
                "5.00",
                "1.00",
                "5.00",
                "3.00",
                "15.00",
                "25.00",
                "5.00",
                "1.00",
            ],
        )

from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_admin_profile,
    create_student_profile,
    create_lecturer_profile,
    create_course,
    create_course_obj,
    create_lesson,
    create_technology,
    create_skill,
    create_topic,
    create_review,
    create_purchase,
    create_teaching,
    create_lesson_price_history,
    create_image,
    create_video,
    create_module,
    create_schedule,
    create_reservation,
)
from .helpers import (
    login,
    is_data_match,
    get_course,
    get_lesson,
    get_module,
    get_technology,
    get_skill,
    get_topic,
    courses_number,
    get_course_modules,
    get_course_skills,
    get_course_topics,
)
from django.contrib import auth
import json
from base64 import b64encode
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class CourseTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/courses"
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
            first_name="l1_first_name",
            last_name="l1_last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="l2_first_name",
            last_name="l2_last_name",
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

        self.purchase = create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
        )

        self.schedule = create_schedule(
            self.lecturer_profile_1,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                - timedelta(hours=25)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                - timedelta(hours=24)
            ),
            lesson=self.lesson_1,
        )

        create_reservation(
            student=self.profile,
            lesson=self.lesson_1,
            schedule=self.schedule,
            purchase=self.purchase,
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

        self.user_columns = ["first_name", "last_name", "email"]
        self.profile_columns = ["uuid"]

        self.new_course = create_course_obj(
            title="Javascript course",
            description="course_description",
            level="E",
            modules=[self.module_3.id, self.module_2.id],
            skills=[self.skill_1.id, self.skill_2.id],
            topics=[
                self.topic_1.id,
                self.topic_2.id,
            ],
            image=b64encode(create_image().read()),
            video=b64encode(create_video().read()),
        )

        self.amend_course = create_course_obj(
            title="Python for beginners course",
            description="course_description_other",
            level="Z",
            modules=[self.module_3.id, self.module_2.id],
            skills=[self.skill_1.id],
            topics=[self.topic_2.id],
            image=b64encode(create_image().read()),
            video=b64encode(create_video().read()),
        )

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

    def test_get_courses_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
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

    def test_get_course_inactive(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        self.course.active = False
        self.course.save()

        response = self.client.get(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_course_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course_data = json.loads(response.content)
        modules_data = course_data.pop("modules")
        technology_data = course_data.pop("technologies")
        skills_data = course_data.pop("skills")
        topics_data = course_data.pop("topics")
        course_data.pop("duration")
        course_data.pop("lecturers")
        price = course_data.pop("price")
        previous_price = course_data.pop("previous_price")
        lowest_30_days_price = course_data.pop("lowest_30_days_price")
        progress = course_data.pop("progress")
        rating = course_data.pop("rating")
        rating_count = course_data.pop("rating_count")
        students_count = course_data.pop("students_count")
        self.assertTrue(is_data_match(get_course(self.course.id), course_data))
        self.assertEqual(price, 12.98)
        self.assertEqual(previous_price, 12.99)
        self.assertEqual(lowest_30_days_price, 10.99)
        self.assertEqual(progress, None)
        self.assertEqual(rating, 4.0)
        self.assertEqual(rating_count, 3)
        self.assertEqual(students_count, 2)
        for module_data in modules_data:
            price = module_data.pop("price")
            previous_price = module_data.pop("previous_price")
            lowest_30_days_price = module_data.pop("lowest_30_days_price")
            progress = module_data.pop("progress")
            lessons_data = module_data.pop("lessons")

            self.assertEqual(price, 12.98)
            self.assertEqual(previous_price, 12.99)
            self.assertEqual(lowest_30_days_price, 10.99)
            self.assertEqual(progress, None)
            self.assertTrue(is_data_match(get_module(module_data["id"]), module_data))

            for lesson_data in lessons_data:
                previous_price = lesson_data.pop("previous_price")
                lowest_30_days_price = lesson_data.pop("lowest_30_days_price")
                progress = lesson_data.pop("progress")

                self.assertTrue(
                    is_data_match(get_lesson(lesson_data["id"]), lesson_data)
                )

                if lesson_data["id"] == self.review_1.lesson.id:
                    self.assertEqual(previous_price, None)
                    self.assertEqual(lowest_30_days_price, None)
                    self.assertEqual(progress, None)
                elif lesson_data["id"] == self.review_3.lesson.id:
                    self.assertEqual(previous_price, 3.0)
                    self.assertEqual(lowest_30_days_price, 1.0)
                    self.assertEqual(progress, None)
                else:
                    self.assertEqual(previous_price, 2)
                    self.assertEqual(lowest_30_days_price, 2)
                    self.assertEqual(progress, None)

        for technology in technology_data:
            self.assertTrue(is_data_match(get_technology(technology["id"]), technology))
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
        modules_data = course_data.pop("modules")
        technology_data = course_data.pop("technologies")
        skills_data = course_data.pop("skills")
        topics_data = course_data.pop("topics")
        course_data.pop("duration")
        course_data.pop("lecturers")
        price = course_data.pop("price")
        previous_price = course_data.pop("previous_price")
        lowest_30_days_price = course_data.pop("lowest_30_days_price")
        progress = course_data.pop("progress")
        rating = course_data.pop("rating")
        rating_count = course_data.pop("rating_count")
        students_count = course_data.pop("students_count")
        self.assertTrue(is_data_match(get_course(self.course.id), course_data))
        self.assertEqual(price, 12.98)
        self.assertEqual(previous_price, 12.99)
        self.assertEqual(lowest_30_days_price, 10.99)
        self.assertEqual(progress, 0.5)
        self.assertEqual(rating, 4.0)
        self.assertEqual(rating_count, 3)
        self.assertEqual(students_count, 2)
        for module_data in modules_data:
            price = module_data.pop("price")
            previous_price = module_data.pop("previous_price")
            lowest_30_days_price = module_data.pop("lowest_30_days_price")
            progress = module_data.pop("progress")
            lessons_data = module_data.pop("lessons")

            self.assertEqual(price, 12.98)
            self.assertEqual(previous_price, 12.99)
            self.assertEqual(lowest_30_days_price, 10.99)
            self.assertEqual(progress, 0.5)
            self.assertTrue(is_data_match(get_module(module_data["id"]), module_data))

            for lesson_data in lessons_data:
                previous_price = lesson_data.pop("previous_price")
                lowest_30_days_price = lesson_data.pop("lowest_30_days_price")
                progress = lesson_data.pop("progress")

                self.assertTrue(
                    is_data_match(get_lesson(lesson_data["id"]), lesson_data)
                )

                if lesson_data["id"] == self.review_1.lesson.id:
                    self.assertEqual(previous_price, None)
                    self.assertEqual(lowest_30_days_price, None)
                    self.assertEqual(progress, 1.0)
                elif lesson_data["id"] == self.review_3.lesson.id:
                    self.assertEqual(previous_price, 3.0)
                    self.assertEqual(lowest_30_days_price, 1.0)
                    self.assertEqual(progress, 0.0)
                else:
                    self.assertEqual(previous_price, 2)
                    self.assertEqual(lowest_30_days_price, 2)
                    self.assertEqual(progress, 0.0)

        for technology in technology_data:
            self.assertTrue(is_data_match(get_technology(technology["id"]), technology))
        for skill_data in skills_data:
            self.assertTrue(is_data_match(get_skill(skill_data["id"]), skill_data))
        for topic_data in topics_data:
            self.assertTrue(is_data_match(get_topic(topic_data["id"]), topic_data))

    def test_get_course_authenticated_2(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.course_2.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course_data = json.loads(response.content)
        modules_data = course_data.pop("modules")
        technology_data = course_data.pop("technologies")
        skills_data = course_data.pop("skills")
        topics_data = course_data.pop("topics")
        course_data.pop("duration")
        course_data.pop("lecturers")
        price = course_data.pop("price")
        previous_price = course_data.pop("previous_price")
        lowest_30_days_price = course_data.pop("lowest_30_days_price")
        progress = course_data.pop("progress")
        rating = course_data.pop("rating")
        rating_count = course_data.pop("rating_count")
        students_count = course_data.pop("students_count")
        self.assertTrue(is_data_match(get_course(self.course_2.id), course_data))
        self.assertEqual(price, 12.98)
        self.assertEqual(previous_price, None)
        self.assertEqual(lowest_30_days_price, None)
        self.assertEqual(progress, 0.0)
        self.assertEqual(rating, None)
        self.assertEqual(rating_count, 0)
        self.assertEqual(students_count, 0)
        for module_data in modules_data:
            price = module_data.pop("price")
            previous_price = module_data.pop("previous_price")
            lowest_30_days_price = module_data.pop("lowest_30_days_price")
            progress = module_data.pop("progress")
            lessons_data = module_data.pop("lessons")

            self.assertEqual(price, 12.98)
            self.assertEqual(previous_price, None)
            self.assertEqual(lowest_30_days_price, None)
            self.assertEqual(progress, 0.0)
            self.assertTrue(is_data_match(get_module(module_data["id"]), module_data))

            for lesson_data in lessons_data:
                previous_price = lesson_data.pop("previous_price")
                lowest_30_days_price = lesson_data.pop("lowest_30_days_price")
                progress = lesson_data.pop("progress")

                self.assertTrue(
                    is_data_match(get_lesson(lesson_data["id"]), lesson_data)
                )

                self.assertEqual(previous_price, None)
                self.assertEqual(lowest_30_days_price, None)
                self.assertEqual(progress, 0.0)

        for technology in technology_data:
            self.assertTrue(is_data_match(get_technology(technology["id"]), technology))
        for skill_data in skills_data:
            self.assertTrue(is_data_match(get_skill(skill_data["id"]), skill_data))
        for topic_data in topics_data:
            self.assertTrue(is_data_match(get_topic(topic_data["id"]), topic_data))

    def test_get_course_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.course_2.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course_data = json.loads(response.content)
        modules_data = course_data.pop("modules")
        technology_data = course_data.pop("technologies")
        skills_data = course_data.pop("skills")
        topics_data = course_data.pop("topics")
        course_data.pop("duration")
        course_data.pop("lecturers")
        price = course_data.pop("price")
        previous_price = course_data.pop("previous_price")
        lowest_30_days_price = course_data.pop("lowest_30_days_price")
        progress = course_data.pop("progress")
        rating = course_data.pop("rating")
        rating_count = course_data.pop("rating_count")
        students_count = course_data.pop("students_count")
        self.assertTrue(is_data_match(get_course(self.course_2.id), course_data))
        self.assertEqual(price, 12.98)
        self.assertEqual(previous_price, None)
        self.assertEqual(lowest_30_days_price, None)
        self.assertEqual(progress, None)
        self.assertEqual(rating, None)
        self.assertEqual(rating_count, 0)
        self.assertEqual(students_count, 0)
        for module_data in modules_data:
            price = module_data.pop("price")
            previous_price = module_data.pop("previous_price")
            lowest_30_days_price = module_data.pop("lowest_30_days_price")
            progress = module_data.pop("progress")
            lessons_data = module_data.pop("lessons")

            self.assertEqual(price, 12.98)
            self.assertEqual(previous_price, None)
            self.assertEqual(lowest_30_days_price, None)
            self.assertEqual(progress, None)
            self.assertTrue(is_data_match(get_module(module_data["id"]), module_data))

            for lesson_data in lessons_data:
                previous_price = lesson_data.pop("previous_price")
                lowest_30_days_price = lesson_data.pop("lowest_30_days_price")
                progress = lesson_data.pop("progress")

                self.assertTrue(
                    is_data_match(get_lesson(lesson_data["id"]), lesson_data)
                )

                self.assertEqual(previous_price, None)
                self.assertEqual(lowest_30_days_price, None)
                self.assertEqual(progress, None)

        for technology in technology_data:
            self.assertTrue(is_data_match(get_technology(technology["id"]), technology))
        for skill_data in skills_data:
            self.assertTrue(is_data_match(get_skill(skill_data["id"]), skill_data))
        for topic_data in topics_data:
            self.assertTrue(is_data_match(get_topic(topic_data["id"]), topic_data))

    def test_create_course_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_course
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 3)

    def test_create_course_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_course
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 3)

    def test_create_course_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_course
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(courses_number(), 4)
        course_data = json.loads(response.content)
        modules_ids = course_data.pop("modules")
        skills_ids = course_data.pop("skills")
        topics_ids = course_data.pop("topics")
        self.assertTrue(is_data_match(get_course(course_data["id"]), course_data))
        self.assertEqual(
            sorted(
                list(
                    set(
                        [
                            record.module.id
                            for record in get_course_modules(course_data["id"])
                        ]
                    )
                )
            ),
            sorted(modules_ids),
        )
        self.assertEqual(
            sorted(
                [record.skill.id for record in get_course_skills(course_data["id"])]
            ),
            sorted(skills_ids),
        )
        self.assertEqual(
            sorted(
                [record.topic.id for record in get_course_topics(course_data["id"])]
            ),
            sorted(topics_ids),
        )

    def test_create_course_without_lesson(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_course
        del data["modules"]
        data["modules"] = []

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)

    def test_create_course_without_skills(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_course
        del data["skills"]
        data["skills"] = []

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)

    def test_create_course_without_topics(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.new_course
        del data["topics"]
        data["topics"] = []

        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)

    def test_update_course_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_course
        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 3)

    def test_update_course_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_course
        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 3)

    def test_update_course_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_course
        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(courses_number(), 3)
        course_data = json.loads(response.content)
        modules_ids = course_data.pop("modules")
        skills_ids = course_data.pop("skills")
        topics_ids = course_data.pop("topics")
        self.assertTrue(is_data_match(get_course(course_data["id"]), course_data))
        self.assertEqual(
            sorted(
                list(
                    set(
                        [
                            record.module.id
                            for record in get_course_modules(course_data["id"])
                        ]
                    )
                )
            ),
            sorted(modules_ids),
        )
        self.assertEqual(
            sorted(
                [record.skill.id for record in get_course_skills(course_data["id"])]
            ),
            sorted(skills_ids),
        )
        self.assertEqual(
            sorted(
                [record.topic.id for record in get_course_topics(course_data["id"])]
            ),
            sorted(topics_ids),
        )

    def test_update_course_without_modules(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_course
        del data["modules"]
        data["modules"] = []

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)

    def test_update_course_without_skills(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_course
        del data["skills"]
        data["skills"] = []

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)

    def test_update_course_without_topics(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = self.amend_course
        del data["topics"]
        data["topics"] = []

        response = self.client.put(f"{self.endpoint}/{self.course.id}", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)

    def test_delete_course_unauthorized(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)

        response = self.client.delete(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 3)

    def test_delete_course_not_admin(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)

        response = self.client.delete(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(courses_number(), 3)

    def test_delete_course_active_authorized(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)

        response = self.client.delete(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(courses_number(), 3)

    def test_delete_course_authorized(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)

        self.course.active = False
        self.course.save()

        response = self.client.delete(f"{self.endpoint}/{self.course.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(courses_number(), 2)


class BestCourseTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/best-courses"
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
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
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

        self.user_columns = ["first_name", "last_name", "email"]
        self.profile_columns = ["uuid"]

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

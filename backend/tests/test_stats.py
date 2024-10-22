from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_student_profile,
    create_lecturer_profile,
    create_course,
    create_lesson,
    create_technology,
    create_skill,
    create_topic,
    create_review,
    create_purchase,
    create_module,
    create_payment,
)
import json


class StatsTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/stats"
        self.user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="user@example.com",
            password="TestPassword123",
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
            password="TestPassword123",
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
        )

        self.technology_1 = create_technology(name="Python")

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

        self.skill_1 = create_skill(name="coding")
        self.skill_2 = create_skill(name="IDE")

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
            skills=[self.skill_1, self.skill_2],
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
            lesson=self.lesson_1,
            student=self.profile_2,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )
        create_purchase(
            lesson=self.lesson_1,
            student=self.profile_3,
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
            lesson=self.lesson_2,
            student=self.profile_2,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )
        create_purchase(
            lesson=self.lesson_2,
            student=self.profile_3,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
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

    def test_get_stats_1(self):
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "students_count": 3,
                "course_count": 1,
                "lessons_count": 4,
                "technology_count": 1,
                "lecturers_count": 1,
                "purchase_count": 7,
                "hours_sum": 3.0,
                "rating": 4.0,
                "rating_count": 6,
            },
        )

    def test_get_stats_2(self):
        # get data
        self.review_1.delete()
        self.review_2.delete()
        self.review_3.delete()
        self.review_4.delete()
        self.review_5.delete()
        self.review_6.delete()
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "students_count": 3,
                "course_count": 1,
                "lessons_count": 4,
                "technology_count": 1,
                "lecturers_count": 1,
                "purchase_count": 7,
                "hours_sum": 3.0,
                "rating": 0,
                "rating_count": 0,
            },
        )

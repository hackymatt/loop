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
    create_purchase,
    create_teaching,
    create_schedule,
    create_reservation,
    create_review,
    create_coupon,
)
from .helpers import login
import json
from django.contrib import auth
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class PurchaseTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/purchase"
        self.data = {
            "email": "user@example.com",
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

        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_profile(user=self.lecturer_user, user_type="W")

        self.technology_1 = create_technology(name="Python")
        self.technology_2 = create_technology(name="JS")
        self.technology_3 = create_technology(name="VBA")

        # course 1
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

        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
            level="Podstawowy",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            lessons=[self.lesson_1, self.lesson_2],
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

        for lesson in self.course_1.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile,
                lesson=lesson,
            )

        self.schedules = []
        for i in range(-10, 100):
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile,
                    start_time=make_aware(
                        datetime.now().replace(minute=30, second=0, microsecond=0)
                        + timedelta(minutes=30 * i)
                    ),
                    end_time=make_aware(
                        datetime.now().replace(minute=30, second=0, microsecond=0)
                        + timedelta(minutes=30 * (i + 1))
                    ),
                )
            )
        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_1,
            schedule=self.schedules[len(self.schedules) - 3],
            purchase=self.purchase_1,
        )
        self.purchase_2 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_2,
            schedule=self.schedules[0],
            purchase=self.purchase_2,
        )

        # course 2
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
        self.lesson_5 = create_lesson(
            title="JS lesson 3",
            description="bbbb",
            duration="120",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )
        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            level="Zaawansowany",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            lessons=[self.lesson_3, self.lesson_4, self.lesson_5],
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

        create_review(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )

        # course 3
        self.lesson_6 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )
        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            level="Ekspert",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            lessons=[self.lesson_6],
        )

        self.coupon_1 = create_coupon(
            code="aaaaaaaaa",
            discount=1,
            is_percentage=False,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
            min_total=0,
        )
        self.coupon_2 = create_coupon(
            code="bbbbbbbbb",
            discount=1,
            is_percentage=True,
            all_users=True,
            is_infinite=True,
            active=True,
            expiration_date=make_aware(datetime.now() + timedelta(days=10)),
            min_total=0,
        )

    def test_get_purchase_unauthenticated(self):
        # login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_purchase_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        self.assertEqual(records_count, 6)

    def test_create_purchase_unauthenticated(self):
        # login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lessons": [
                {
                    "lesson": self.lesson_6.id,
                }
            ],
            "coupon": "",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_purchase_inactive_lesson(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lessons": [
                {
                    "lesson": self.lesson_6.id,
                },
                {
                    "lesson": self.lesson_5.id,
                },
            ],
            "coupon": "",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_purchase_incorrect_coupon(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.lesson_5.active = True
        self.lesson_5.save()
        self.lesson_6.active = True
        self.lesson_6.save()
        data = {
            "lessons": [
                {
                    "lesson": self.lesson_6.id,
                },
                {
                    "lesson": self.lesson_5.id,
                },
            ],
            "coupon": "incorrect",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_purchase_payment_error(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.lesson_5.active = True
        self.lesson_5.price = 1
        self.lesson_5.save()
        self.lesson_6.active = True
        self.lesson_6.price = 0
        self.lesson_6.save()
        data = {
            "lessons": [
                {
                    "lesson": self.lesson_6.id,
                },
                {
                    "lesson": self.lesson_5.id,
                },
            ],
            "coupon": self.coupon_1.code,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_purchase_1_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.lesson_5.active = True
        self.lesson_5.save()
        self.lesson_6.active = True
        self.lesson_6.save()

        data = {
            "lessons": [
                {
                    "lesson": self.lesson_6.id,
                },
                {
                    "lesson": self.lesson_5.id,
                },
            ],
            "coupon": self.coupon_1.code,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase_2_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.lesson_5.active = True
        self.lesson_5.save()
        self.lesson_6.active = True
        self.lesson_6.save()

        data = {
            "lessons": [
                {
                    "lesson": self.lesson_6.id,
                },
                {
                    "lesson": self.lesson_5.id,
                },
            ],
            "coupon": self.coupon_2.code,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase_3_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.lesson_5.active = True
        self.lesson_5.save()
        self.lesson_6.active = True
        self.lesson_6.save()

        data = {
            "lessons": [
                {
                    "lesson": self.lesson_6.id,
                },
                {
                    "lesson": self.lesson_5.id,
                },
            ],
            "coupon": "",
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

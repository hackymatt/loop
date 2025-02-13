from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.test import TestCase
from unittest.mock import patch
from .factory import (
    create_user,
    create_profile,
    create_student_profile,
    create_lecturer_profile,
    create_admin_profile,
    create_course,
    create_lesson,
    create_technology,
    create_tag,
    create_topic,
    create_candidate,
    create_purchase,
    create_teaching,
    create_schedule,
    create_reservation,
    create_review,
    create_coupon,
    create_meeting,
    create_module,
    create_payment,
    create_recording,
)
from .helpers import (
    login,
    mock_register_payment,
    mock_send_message,
    mock_upload_invoice,
    notifications_number,
    is_float,
)
import json
from django.contrib import auth
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from config_global import CANCELLATION_TIME
import uuid
from utils.przelewy24.payment import Przelewy24Api
from utils.google.gmail import GmailApi
from purchase.utils import Invoice


class PurchaseTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/purchases"
        self.client = APIClient()
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
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="user2@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.profile = create_student_profile(profile=create_profile(user=self.user))
        self.profile_2 = create_student_profile(
            profile=create_profile(user=self.user_2)
        )

        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
        )
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

        self.candidate_1 = create_candidate(name="No tech knowledge")
        self.candidate_2 = create_candidate(name="Tech interested")

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
        )

        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
            overview="Python is great language",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_1],
        )

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )

        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )

        for module in self.course_1.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile,
                    lesson=lesson,
                )

        self.schedules = []
        for i in range(-10, 100):
            schedule = create_schedule(
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
            if (schedule.start_time - make_aware(datetime.now())) < timedelta(
                hours=CANCELLATION_TIME
            ):
                id = str(uuid.uuid4())
                schedule.meeting = create_meeting(
                    event_id=id, url=f"https://example.com/{id}"
                )
                schedule.save()

            self.schedules.append(schedule)
        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile_2,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )
        meeting = create_meeting(event_id="test_event", url="https://example.com")
        self.schedules[len(self.schedules) - 3].meeting = meeting
        self.schedules[len(self.schedules) - 3].save()
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
            payment=create_payment(amount=self.lesson_2.price),
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_2,
            schedule=self.schedules[0],
            purchase=self.purchase_2,
        )
        create_recording(schedule=self.schedules[0])

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
        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_3, self.lesson_4, self.lesson_5]
        )

        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            overview="Learn more",
            level="Zaawansowany",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_2],
        )

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_4.price,
            payment=create_payment(amount=self.lesson_4.price),
        )

        create_review(
            lesson=self.lesson_3,
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
        self.module_3 = create_module(title="Module 3", lessons=[self.lesson_6])

        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            overview="Learn more",
            level="Ekspert",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_3],
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
        # no login
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
        self.assertEqual(records_count, 5)

    def test_get_purchase_authenticated_admin(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        self.assertEqual(records_count, 6)

    def test_create_purchase_unauthenticated(self):
        # no login
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

    @patch.object(Przelewy24Api, "register")
    def test_create_purchase_1_authenticated(self, register_mock):
        mock_register_payment(mock=register_mock)
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

    @patch.object(Przelewy24Api, "register")
    def test_create_purchase_2_authenticated(self, register_mock):
        mock_register_payment(mock=register_mock)
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

    @patch.object(Przelewy24Api, "register")
    def test_create_purchase_3_authenticated(self, register_mock):
        mock_register_payment(mock=register_mock)
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

    @patch.object(Invoice, "_upload")
    @patch.object(GmailApi, "_send_message")
    def test_create_purchase_4_authenticated(
        self, _send_message_mock, upload_invoice_mock
    ):
        mock_send_message(mock=_send_message_mock)
        mock_upload_invoice(mock=upload_invoice_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        self.lesson_5.active = True
        self.lesson_5.save()
        self.lesson_6.active = True
        self.lesson_6.save()

        self.coupon_1.discount = 1000
        self.coupon_1.save()

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
        self.assertEqual(notifications_number(), 1)
        self.assertEqual(_send_message_mock.call_count, 1)
        self.assertEqual(upload_invoice_mock.call_count, 1)


class PurchaseFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/purchases"
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
        self.profile = create_student_profile(profile=create_profile(user=self.user))

        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
        )

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
        self.lesson_3 = create_lesson(
            title="Python lesson 3",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_1],
        )

        self.topic_1 = create_topic(name="You will learn how to code")
        self.topic_2 = create_topic(name="You will learn a new IDE")

        self.candidate_1 = create_candidate(name="No tech knowledge")
        self.candidate_2 = create_candidate(name="Tech interested")

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2, self.lesson_3]
        )

        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
            overview="Python is great language",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_1],
        )

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )

        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )

        for module in self.course_1.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile,
                    lesson=lesson,
                )

        self.schedules = []
        for i in range(-100, 10):
            schedule = create_schedule(
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
            if (schedule.start_time - make_aware(datetime.now())) < timedelta(
                hours=CANCELLATION_TIME
            ):
                id = str(uuid.uuid4())
                schedule.meeting = create_meeting(
                    event_id=id, url=f"https://example.com/{id}"
                )
                schedule.save()

            self.schedules.append(schedule)

        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_1,
            schedule=self.schedules[len(self.schedules) - 3],
            purchase=self.purchase_1,
        )
        self.schedules[len(self.schedules) - 3].lesson = self.lesson_1
        self.schedules[len(self.schedules) - 3].save()
        self.purchase_2 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_2,
            schedule=self.schedules[0],
            purchase=self.purchase_2,
        )
        self.schedules[0].lesson = self.lesson_2
        self.schedules[0].save()
        self.purchase_3 = create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_3,
            schedule=self.schedules[1],
            purchase=self.purchase_3,
        )
        self.schedules[1].lesson = self.lesson_3
        self.schedules[1].save()
        create_review(
            lesson=self.lesson_2,
            student=self.profile,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )

        # course 2
        self.lesson_4 = create_lesson(
            title="JS lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_2],
        )
        self.lesson_5 = create_lesson(
            title="JS lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )
        self.lesson_6 = create_lesson(
            title="JS lesson 3",
            description="bbbb",
            duration="120",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )

        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_4, self.lesson_5, self.lesson_6]
        )

        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            overview="Learn more",
            level="Zaawansowany",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_2],
        )

        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_purchase(
            lesson=self.lesson_5,
            student=self.profile,
            price=self.lesson_4.price,
            payment=create_payment(amount=self.lesson_4.price),
        )

        create_review(
            lesson=self.lesson_4,
            student=self.profile,
            lecturer=self.lecturer_profile,
            rating=5,
            review="Great lesson.",
        )

        # course 3
        self.lesson_7 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
        )

        self.module_3 = create_module(title="Module 3", lessons=[self.lesson_7])

        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            overview="Learn more",
            level="Ekspert",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_3],
        )

    def test_lesson_title_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        lesson_title = self.lesson_1.title[1:5]
        response = self.client.get(f"{self.endpoint}?lesson_title={lesson_title}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 6)
        titles = list(
            set([lesson_title in record["lesson"]["title"] for record in results])
        )
        self.assertTrue(len(titles) == 1)
        self.assertTrue(titles[0])

    def test_price_from_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 5
        response = self.client.get(f"{self.endpoint}?price_from={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        prices = list(set([float(record["price"]) >= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_price_to_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        price = 10
        response = self.client.get(f"{self.endpoint}?price_to={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 8)
        prices = list(set([float(record["price"]) <= price for record in results]))
        self.assertTrue(len(prices) == 1)
        self.assertTrue(prices[0])

    def test_lesson_status_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        lesson_status = "potwierdzona"
        response = self.client.get(f"{self.endpoint}?lesson_status={lesson_status}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        statuses = list(
            set([record["lesson_status"] == lesson_status for record in results])
        )
        self.assertTrue(len(statuses) == 1)
        self.assertTrue(statuses[0])

    def test_review_status_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        review_status = "oczekujące"
        response = self.client.get(f"{self.endpoint}?review_status={review_status}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 1)
        statuses = list(
            set([record["review_status"] == review_status for record in results])
        )
        self.assertTrue(len(statuses) == 1)
        self.assertTrue(statuses[0])

    def test_review_status_exclude_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        review_status = "brak"
        response = self.client.get(
            f"{self.endpoint}?review_status_exclude={review_status}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 2)
        statuses = list(
            set([record["review_status"] == review_status for record in results])
        )
        self.assertTrue(len(statuses) == 1)
        self.assertFalse(statuses[0])

    def test_lecturer_id_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        id = self.lecturer_profile.id

        response = self.client.get(f"{self.endpoint}?lecturer_id={id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 3)
        ids = list(
            set(
                [
                    str(record["reservation"]["schedule"]["lecturer"]["id"]) == str(id)
                    for record in results
                ]
            )
        )
        self.assertTrue(len(ids) == 1)
        self.assertTrue(ids[0])

    def test_created_at_filter(self):
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        date = str(self.course_1.created_at)[0:10]
        response = self.client.get(f"{self.endpoint}?created_at={date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        records_count = data["records_count"]
        results = data["results"]
        self.assertEqual(records_count, 8)
        dates = list(set([date in record["created_at"] for record in results]))
        self.assertTrue(len(dates) == 1)
        self.assertTrue(dates[0])


class PurchaseOrderTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/purchases"
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
        self.profile = create_student_profile(profile=create_profile(user=self.user))

        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
        )

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

        self.candidate_1 = create_candidate(name="No tech knowledge")
        self.candidate_2 = create_candidate(name="Tech interested")

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
        )

        self.course_1 = create_course(
            title="Python Beginner",
            description="Learn Python today",
            overview="Python is great language",
            level="Podstawowy",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_1],
        )

        create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
        )

        create_purchase(
            lesson=self.lesson_2,
            student=self.profile,
            price=self.lesson_2.price,
            payment=create_payment(amount=self.lesson_2.price),
        )

        for module in self.course_1.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile,
                    lesson=lesson,
                )

        self.schedules = []
        for i in range(-100, 10):
            schedule = create_schedule(
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
            if (schedule.start_time - make_aware(datetime.now())) < timedelta(
                hours=CANCELLATION_TIME
            ):
                id = str(uuid.uuid4())
                schedule.meeting = create_meeting(
                    event_id=id, url=f"https://example.com/{id}"
                )
                schedule.save()

            self.schedules.append(schedule)
        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
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
            payment=create_payment(amount=self.lesson_2.price),
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
        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_3, self.lesson_4, self.lesson_5]
        )

        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            overview="Learn more",
            level="Zaawansowany",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_2],
        )

        create_purchase(
            lesson=self.lesson_3,
            student=self.profile,
            price=self.lesson_3.price,
            payment=create_payment(amount=self.lesson_3.price),
        )
        create_purchase(
            lesson=self.lesson_4,
            student=self.profile,
            price=self.lesson_4.price,
            payment=create_payment(amount=self.lesson_4.price),
        )

        create_review(
            lesson=self.lesson_3,
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
        self.module_3 = create_module(title="Module 3", lessons=[self.lesson_6])

        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            overview="Learn more",
            level="Ekspert",
            tags=[self.tag_1, self.tag_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            candidates=[
                self.candidate_1,
                self.candidate_2,
            ],
            modules=[self.module_3],
        )

        self.fields = [
            "lesson_title",
            "price",
            "lesson_status",
            "review_status",
            "lecturer_id",
            "created_at",
        ]

    def test_ordering(self):
        for field in self.fields:
            login(self, self.data["email"], self.data["password"])
            self.assertTrue(auth.get_user(self.client).is_authenticated)
            # get data
            response = self.client.get(f"{self.endpoint}?sort_by={field}")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            data = json.loads(response.content)
            count = data["records_count"]
            results = data["results"]
            self.assertEqual(count, 6)
            if "_title" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course["reservation"]
                    for course in results
                    if course["reservation"] is not None
                ]
                parent_objects = [
                    course["schedule"]
                    for course in parent_objects
                    if course["schedule"] is not None
                ]
                parent_objects = [
                    course[field1]
                    for course in parent_objects
                    if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
            else:
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
            self.assertEqual(count, 6)
            if "_title" in field:
                field1, field2 = field.split("_")
                field_values = [course[field1][field2] for course in results]
            elif "_id" in field:
                field1, field2 = field.split("_")
                parent_objects = [
                    course["reservation"]
                    for course in results
                    if course["reservation"] is not None
                ]
                parent_objects = [
                    course["schedule"]
                    for course in parent_objects
                    if course["schedule"] is not None
                ]
                parent_objects = [
                    course[field1]
                    for course in parent_objects
                    if course[field1] is not None
                ]
                field_values = [
                    parent_object[field2] for parent_object in parent_objects
                ]
            else:
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

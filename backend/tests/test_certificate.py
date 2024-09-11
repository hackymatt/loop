from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase
from unittest.mock import patch
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
    create_purchase,
    create_schedule,
    create_teaching,
    create_reservation,
    create_module,
    create_certificate,
)
from .helpers import login, mock_send_message, certificates_number, notifications_number
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
import uuid
from utils.google.gmail import GmailApi
from certificate.utils import generate_certificates


class CertificateTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/certificates"
        self.data = {
            "email": "user@example.com",
            "password": "TestPassword123",
        }
        self.user_1 = create_user(
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

        self.lecturer_data = {
            "email": "lecturer_1@example.com",
            "password": "TestPassword123",
        }
        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.lecturer_data["email"],
            password=self.lecturer_data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
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

        for module in self.course.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile,
                    lesson=lesson,
                )

        self.schedules = []
        for i in range(10):
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

        self.schedules.append(
            create_schedule(
                lecturer=self.lecturer_profile,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * 100)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (100 + 1))
                ),
            )
        )

        self.schedules.append(
            create_schedule(
                lecturer=self.lecturer_profile,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * 102)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (102 + 1))
                ),
            )
        )

        self.schedules.append(
            create_schedule(
                lecturer=self.lecturer_profile,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * 103)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (103 + 1))
                ),
            )
        )
        self.long_timeslot = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 50)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 53)
            ),
            lesson=self.lesson_1,
        )
        self.long_timeslot_2 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 30)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 33)
            ),
            lesson=self.lesson_1,
        )

        self.long_timeslot_3 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 400)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 403)
            ),
            lesson=self.lesson_4,
        )

        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile_1,
            price=self.lesson_1.price,
        )
        self.reservation_1 = create_reservation(
            student=self.profile_1,
            lesson=self.lesson_1,
            schedule=self.schedules[0],
            purchase=self.purchase_1,
        )
        self.schedules[0].lesson = self.lesson_1
        self.schedules[0].save()
        self.purchase_2 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile_2,
            price=self.lesson_2.price,
        )
        self.reservation_2 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_2,
            schedule=self.schedules[2],
            purchase=self.purchase_2,
        )
        self.schedules[2].lesson = self.lesson_2
        self.schedules[2].save()
        self.purchase_3 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile_2,
            price=self.lesson_1.price,
        )
        self.reservation_3 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_1,
            schedule=self.schedules[0],
            purchase=self.purchase_3,
        )
        self.purchase_4 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile_1,
            price=self.lesson_2.price,
        )
        self.reservation_4 = create_reservation(
            student=self.profile_1,
            lesson=self.lesson_2,
            schedule=self.schedules[6],
            purchase=self.purchase_4,
        )
        self.schedules[6].lesson = self.lesson_2
        self.schedules[6].save()
        self.purchase_5 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile_2,
            price=self.lesson_2.price,
        )
        self.reservation_5 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_2,
            schedule=self.long_timeslot_2,
            purchase=self.purchase_5,
        )
        self.long_timeslot_2.lesson = self.lesson_1
        self.long_timeslot_2.save()
        self.purchase_6 = create_purchase(
            lesson=self.lesson_4,
            student=self.profile_1,
            price=self.lesson_4.price,
        )
        self.reservation_6 = create_reservation(
            student=self.profile_1,
            lesson=self.lesson_4,
            schedule=self.long_timeslot_3,
            purchase=self.purchase_6,
        )
        self.long_timeslot_3.lesson = self.lesson_4
        self.long_timeslot_3.save()

        self.certificate = create_certificate(
            entity_type="L",
            entity=self.lesson_1,
            student=self.profile_2,
        )
        self.certificate_2 = create_certificate(
            entity_type="M",
            entity=self.module_1,
            student=self.profile_1,
        )
        self.certificate_3 = create_certificate(
            entity_type="K",
            entity=self.course,
            student=self.profile_1,
        )

    def test_get_certificates_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_certificates_not_authorized(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_certificates_authorized(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        results = data["results"]
        count = data["records_count"]
        self.assertEqual(count, 2)
        self.assertEqual(
            list(results[0].keys()), ["id", "title", "type", "completed_at"]
        )


class CertificateInfoTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/certificate"
        self.data = {
            "email": "user@example.com",
            "password": "TestPassword123",
        }
        self.user_1 = create_user(
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
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
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

        for module in self.course.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile,
                    lesson=lesson,
                )

        self.schedules = []
        for i in range(10):
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

        self.schedules.append(
            create_schedule(
                lecturer=self.lecturer_profile,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * 100)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (100 + 1))
                ),
            )
        )

        self.schedules.append(
            create_schedule(
                lecturer=self.lecturer_profile,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * 102)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (102 + 1))
                ),
            )
        )

        self.schedules.append(
            create_schedule(
                lecturer=self.lecturer_profile,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * 103)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                    + timedelta(minutes=30 * (103 + 1))
                ),
            )
        )
        self.long_timeslot = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 50)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 53)
            ),
            lesson=self.lesson_1,
        )
        self.long_timeslot_2 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 30)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 33)
            ),
            lesson=self.lesson_1,
        )

        self.long_timeslot_3 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 400)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 403)
            ),
            lesson=self.lesson_4,
        )

        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile_1,
            price=self.lesson_1.price,
        )
        self.reservation_1 = create_reservation(
            student=self.profile_1,
            lesson=self.lesson_1,
            schedule=self.schedules[0],
            purchase=self.purchase_1,
        )
        self.schedules[0].lesson = self.lesson_1
        self.schedules[0].save()
        self.purchase_2 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile_2,
            price=self.lesson_2.price,
        )
        self.reservation_2 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_2,
            schedule=self.schedules[2],
            purchase=self.purchase_2,
        )
        self.schedules[2].lesson = self.lesson_2
        self.schedules[2].save()
        self.purchase_3 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile_2,
            price=self.lesson_1.price,
        )
        self.reservation_3 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_1,
            schedule=self.schedules[0],
            purchase=self.purchase_3,
        )
        self.purchase_4 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile_1,
            price=self.lesson_2.price,
        )
        self.reservation_4 = create_reservation(
            student=self.profile_1,
            lesson=self.lesson_2,
            schedule=self.schedules[6],
            purchase=self.purchase_4,
        )
        self.schedules[6].lesson = self.lesson_2
        self.schedules[6].save()
        self.purchase_5 = create_purchase(
            lesson=self.lesson_2,
            student=self.profile_2,
            price=self.lesson_2.price,
        )
        self.reservation_5 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_2,
            schedule=self.long_timeslot_2,
            purchase=self.purchase_5,
        )
        self.long_timeslot_2.lesson = self.lesson_1
        self.long_timeslot_2.save()
        self.purchase_6 = create_purchase(
            lesson=self.lesson_4,
            student=self.profile_1,
            price=self.lesson_4.price,
        )
        self.reservation_6 = create_reservation(
            student=self.profile_1,
            lesson=self.lesson_4,
            schedule=self.long_timeslot_3,
            purchase=self.purchase_6,
        )
        self.long_timeslot_3.lesson = self.lesson_4
        self.long_timeslot_3.save()

        self.certificate = create_certificate(
            entity_type="L",
            entity=self.lesson_1,
            student=self.profile_2,
        )
        self.certificate_2 = create_certificate(
            entity_type="L",
            entity=self.lesson_4,
            student=self.profile_1,
        )

    def test_incorrect_id(self):
        response = self.client.get(f"{self.endpoint}/{str(uuid.uuid4())}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authorized_user_get_his_certificate(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        response = self.client.get(f"{self.endpoint}/{self.certificate_2.uuid}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "id": str(self.certificate_2.uuid),
                "completed_at": (
                    self.certificate_2.created_at - timedelta(days=1)
                ).strftime("%Y-%m-%d"),
                "duration": int(self.certificate_2.duration),
                "title": self.certificate_2.title,
                "reference_number": "{:05d}".format(self.certificate_2.id),
                "student_full_name": f"{self.certificate_2.student.profile.user.first_name} {self.certificate_2.student.profile.user.last_name}",
                "type": "Lekcja",
                "authorized": True,
            },
        )

    def test_authorized_user_get_not_his_certificate(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        response = self.client.get(f"{self.endpoint}/{self.certificate.uuid}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "id": str(self.certificate.uuid),
                "completed_at": (
                    self.certificate.created_at - timedelta(days=1)
                ).strftime("%Y-%m-%d"),
                "duration": int(self.certificate.duration),
                "title": self.certificate.title,
                "reference_number": "{:05d}".format(self.certificate.id),
                "student_full_name": f"{self.certificate.student.profile.user.first_name} {self.certificate.student.profile.user.last_name}",
                "type": "Lekcja",
            },
        )

    def test_not_authorized_user(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        response = self.client.get(f"{self.endpoint}/{self.certificate.uuid}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "id": str(self.certificate.uuid),
                "completed_at": (
                    self.certificate.created_at - timedelta(days=1)
                ).strftime("%Y-%m-%d"),
                "duration": int(self.certificate.duration),
                "title": self.certificate.title,
                "reference_number": "{:05d}".format(self.certificate.id),
                "student_full_name": f"{self.certificate.student.profile.user.first_name} {self.certificate.student.profile.user.last_name}",
                "type": "Lekcja",
            },
        )


class CertificateGenerateTest(TestCase):
    def setUp(self):
        self.data = {
            "email": "user@example.com",
            "password": "TestPassword123",
        }
        self.user_1 = create_user(
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
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
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
        self.lesson_5 = create_lesson(
            title="JS lesson 3",
            description="bbbb",
            duration="120",
            github_url="https://github.com/loopedupl/lesson",
            price="2.99",
            technologies=[self.technology_2],
        )
        self.lesson_6 = create_lesson(
            title="VBA lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="9.99",
            technologies=[self.technology_3],
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
        self.module_3 = create_module(title="Module 3", lessons=[self.lesson_2])
        self.module_4 = create_module(
            title="Module 4", lessons=[self.lesson_5, self.lesson_6]
        )

        self.course_1 = create_course(
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

        self.course_2 = create_course(
            title="course_title_2",
            description="course_description",
            level="Podstawowy",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            modules=[self.module_1, self.module_3],
        )

        for module in self.course_1.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile,
                    lesson=lesson,
                )

        for lesson in self.module_4.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile,
                lesson=lesson,
            )

        # profile 1 only lesson
        self.purchase_1 = create_purchase(
            lesson=self.lesson_1, student=self.profile_1, price=self.lesson_1.price
        )
        self.schedule_1 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=0, second=0, microsecond=0)
                - timedelta(hours=12)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                - timedelta(hours=12)
            ),
            lesson=self.lesson_1,
        )
        self.reservation_1 = create_reservation(
            student=self.profile_1,
            lesson=self.lesson_1,
            schedule=self.schedule_1,
            purchase=self.purchase_1,
        )

        # profile 2 lesson & module
        self.purchase_2 = create_purchase(
            lesson=self.lesson_2, student=self.profile_2, price=self.lesson_2.price
        )
        self.schedule_2 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=0, second=0, microsecond=0)
                - timedelta(hours=6)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                - timedelta(hours=6)
            ),
            lesson=self.lesson_2,
        )
        self.reservation_2 = create_reservation(
            student=self.profile_2,
            lesson=self.lesson_2,
            schedule=self.schedule_2,
            purchase=self.purchase_2,
        )

        # profile 3 lesson & module & course
        self.purchase_3 = create_purchase(
            lesson=self.lesson_2, student=self.profile_3, price=self.lesson_2.price
        )
        self.schedule_3 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=0, second=0, microsecond=0)
                - timedelta(hours=9)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                - timedelta(hours=9)
            ),
            lesson=self.lesson_2,
        )
        self.reservation_3 = create_reservation(
            student=self.profile_3,
            lesson=self.lesson_2,
            schedule=self.schedule_2,
            purchase=self.purchase_2,
        )
        self.purchase_4 = create_purchase(
            lesson=self.lesson_1, student=self.profile_3, price=self.lesson_1.price
        )
        self.schedule_4 = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=0, second=0, microsecond=0)
                - timedelta(hours=10)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                - timedelta(hours=10)
            ),
            lesson=self.lesson_1,
        )
        self.reservation_4 = create_reservation(
            student=self.profile_3,
            lesson=self.lesson_1,
            schedule=self.schedule_3,
            purchase=self.purchase_3,
        )

    @patch.object(GmailApi, "_send_message")
    def test_generate_certificate(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        self.assertEqual(certificates_number(), 0)
        generate_certificates()
        self.assertEqual(certificates_number(), 8)
        self.assertEqual(_send_message_mock.call_count, 3)
        self.assertEqual(notifications_number(), 3)

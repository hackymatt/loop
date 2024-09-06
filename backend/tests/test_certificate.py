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
    create_purchase,
    create_schedule,
    create_teaching,
    create_reservation,
    create_module,
)
from .helpers import login
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class CertificateTest(APITestCase):
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

    def test_incorrect_reservation_id(self):
        response = self.client.get(
            f"{self.endpoint}/{self.profile_1.profile.uuid}-{999999999999}"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_incorrect_profile_uuid(self):
        profile = self.profile_3.profile
        uuid = profile.uuid
        profile.delete()
        response = self.client.get(f"{self.endpoint}/{uuid}-{self.reservation_1.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_incorrect_profile_reservation_mismatch(self):
        response = self.client.get(
            f"{self.endpoint}/{self.profile_1.profile.uuid}-{self.reservation_2.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authorized_user_get_his_certificate(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        response = self.client.get(
            f"{self.endpoint}/{self.profile_1.profile.uuid}-{self.reservation_1.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "completion_date": datetime.today().strftime("%Y-%m-%d"),
                "lesson_duration": 90,
                "lesson_title": "Python lesson 1",
                "reference_number": "00001",
                "student_name": "first_name last_name",
                "teacher_name": "first_name last_name",
                "authorized": True,
            },
        )

    def test_authorized_user_get_not_his_certificate(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        response = self.client.get(
            f"{self.endpoint}/{self.profile_2.profile.uuid}-{self.reservation_2.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "completion_date": datetime.today().strftime("%Y-%m-%d"),
                "lesson_duration": 30,
                "lesson_title": "Python lesson 2",
                "reference_number": "00008",
                "student_name": "first_name last_name",
                "teacher_name": "first_name last_name",
            },
        )

    def test_not_authorized_user(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        response = self.client.get(
            f"{self.endpoint}/{self.profile_1.profile.uuid}-{self.reservation_1.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(
            data,
            {
                "completion_date": datetime.today().strftime("%Y-%m-%d"),
                "lesson_duration": 90,
                "lesson_title": "Python lesson 1",
                "reference_number": "00031",
                "student_name": "first_name last_name",
                "teacher_name": "first_name last_name",
            },
        )

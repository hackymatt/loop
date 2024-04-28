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
    create_schedule,
    create_schedule_obj,
    create_teaching,
    create_reservation,
)
from .helpers import (
    login,
    schedule_number,
    is_schedule_found,
    emails_sent_number,
    get_mail,
    reservation_number,
)
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class ScheduleTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/schedules"
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
        self.lecturer_data = {
            "email": "lecturer_1@example.com",
            "password": "TestPassword123",
        }
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.lecturer_data["email"],
            password=self.lecturer_data["password"],
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

        for lesson in self.course_1.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile_1,
                lesson=lesson,
            )
            create_teaching(
                lecturer=self.lecturer_profile_2,
                lesson=lesson,
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

        for lesson in self.course_2.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile_1,
                lesson=lesson,
            )
            create_teaching(
                lecturer=self.lecturer_profile_2,
                lesson=lesson,
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

        for lesson in self.course_3.lessons.all():
            create_teaching(
                lecturer=self.lecturer_profile_1,
                lesson=lesson,
            )
            create_teaching(
                lecturer=self.lecturer_profile_2,
                lesson=lesson,
            )

        self.schedules = []

        self.schedules.append(
            create_schedule(
                lecturer=self.admin_profile,
                start_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                ),
                end_time=make_aware(
                    datetime.now().replace(minute=30, second=0, microsecond=0)
                ),
            )
        )

        for i in range(10):
            self.schedules.append(
                create_schedule(
                    lecturer=self.lecturer_profile_1,
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
                    lecturer=self.lecturer_profile_2,
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

        self.delete_schedule = create_schedule(
            lecturer=self.lecturer_profile_1,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 10)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 11)
            ),
            lesson=self.lesson_1,
        )

        self.new_schedule = create_schedule_obj(
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 100)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(minutes=30 * 101)
            ),
        )
        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile,
            price=self.lesson_1.price,
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_1,
            schedule=self.delete_schedule,
            purchase=self.purchase_1,
        )
        self.purchase_2 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile_2,
            price=self.lesson_1.price,
        )
        create_reservation(
            student=self.profile_2,
            lesson=self.lesson_1,
            schedule=self.delete_schedule,
            purchase=self.purchase_2,
        )

    def test_get_schedules_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_schedules_not_lecturer(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_schedules_authenticated(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 11)

    def test_get_schedule_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.schedules[0].id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_schedule_not_admin(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.schedules[0].id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_schedule_authenticated(self):
        # login
        login(self, self.admin_data["email"], self.admin_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}/{self.schedules[0].id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_schedule_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.post(self.endpoint, self.new_schedule)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_schedule_not_lecturer(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.post(self.endpoint, self.new_schedule)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_schedule_authenticated(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.post(self.endpoint, self.new_schedule)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = json.loads(response.content)
        self.assertEqual(
            datetime.strptime(data["start_time"], "%Y-%m-%dT%H:%M:%fZ").strftime(
                "%Y-%m-%dT%H:%M"
            ),
            self.new_schedule["start_time"].strftime("%Y-%m-%dT%H:%M"),
        )
        self.assertEqual(
            datetime.strptime(data["end_time"], "%Y-%m-%dT%H:%M:%fZ").strftime(
                "%Y-%m-%dT%H:%M"
            ),
            self.new_schedule["end_time"].strftime("%Y-%m-%dT%H:%M"),
        )

    def test_delete_schedule_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.delete_schedule.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_schedule_not_lecturer(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.delete_schedule.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_schedule_authenticated_no_lesson(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.schedules[1].id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(is_schedule_found(self.schedules[1].id))
        self.assertEqual(schedule_number(), 21)
        self.assertEqual(emails_sent_number(), 0)

    def test_delete_schedule_authenticated_lesson(self):
        # login
        login(self, self.lecturer_data["email"], self.lecturer_data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.delete(f"{self.endpoint}/{self.delete_schedule.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(is_schedule_found(self.delete_schedule.id))
        self.assertEqual(schedule_number(), 21)
        self.assertEqual(emails_sent_number(), 2)
        email = get_mail(0)
        self.assertEqual(email.to, [self.profile.user.email])
        self.assertEqual(
            email.subject,
            "Twoja lekcja została odwołana.",
        )
        email = get_mail(1)
        self.assertEqual(email.to, [self.profile_2.user.email])
        self.assertEqual(
            email.subject,
            "Twoja lekcja została odwołana.",
        )

from rest_framework import status
from django.test import TestCase
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
)
from .helpers import (
    login,
    get_schedule,
    schedule_number,
    is_schedule_found,
    reservation_number,
    is_reservation_found,
    emails_sent_number,
    get_mail,
)
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from reservation.utils import confirm_reservations


class ReservationTest(APITestCase):
    def setUp(self):
        self.endpoint = "/api/reservation"
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

        self.course = create_course(
            title="course_title",
            description="course_description",
            level="Podstawowy",
            skills=[self.skill_1, self.skill_2],
            topics=[
                self.topic_1,
                self.topic_2,
            ],
            lessons=[self.lesson_1, self.lesson_2, self.lesson_3, self.lesson_4],
        )

        for lesson in self.course.lessons.all():
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

    def test_get_reservation_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_reservation_authenticated(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 3)

    def test_create_reservation_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_1.id,
            "schedule": self.schedules[2].id,
            "purchase": self.purchase_1.id,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reservation_number(), 6)
        self.assertEqual(emails_sent_number(), 0)

    def test_create_reservation_authenticated_not_purchased(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.course.lessons.all()[3].id,
            "schedule": self.schedules[2].id,
            "purchase": self.purchase_1.id,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reservation_number(), 6)
        self.assertEqual(emails_sent_number(), 0)

    def test_create_reservation_authenticated_time_not_available(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_1.id,
            "schedule": self.schedules[len(self.schedules) - 3].id,
            "purchase": self.purchase_1.id,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reservation_number(), 6)
        self.assertEqual(emails_sent_number(), 0)

    def test_create_reservation_authenticated_first_reservation_single_slot(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_2.id,
            "schedule": self.schedules[len(self.schedules) - 1].id,
            "purchase": self.purchase_4.id,
        }
        response = self.client.post(self.endpoint, data)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reservation_number(), 7)
        self.assertEqual(data["lesson"], self.lesson_2.id)
        self.assertEqual(data["schedule"], self.schedules[len(self.schedules) - 1].id)
        self.assertEqual(
            get_schedule(self.schedules[len(self.schedules) - 1].id).lesson,
            self.lesson_2,
        )
        self.assertEqual(schedule_number(), 16)
        self.assertEqual(emails_sent_number(), 2)
        student_email = get_mail(0)
        self.assertEqual(student_email.to, [self.data["email"]])
        self.assertEqual(
            student_email.subject,
            f"Potwierdzenie rezerwacji lekcji {self.lesson_2.title}",
        )
        lecturer_reservation_email = get_mail(1)
        self.assertEqual(
            lecturer_reservation_email.to,
            [
                get_schedule(
                    self.schedules[len(self.schedules) - 1].id
                ).lecturer.profile.user.email
            ],
        )
        self.assertEqual(
            lecturer_reservation_email.subject,
            f"Nowy zapis na lekcję {self.lesson_2.title}",
        )

    def test_create_reservation_authenticated_other_reservation_single_slot(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_2.id,
            "schedule": self.schedules[2].id,
            "purchase": self.purchase_4.id,
        }
        response = self.client.post(self.endpoint, data)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reservation_number(), 7)
        self.assertEqual(data["lesson"], self.lesson_2.id)
        self.assertEqual(data["schedule"], self.schedules[2].id)
        self.assertEqual(get_schedule(self.schedules[2].id).lesson, self.lesson_2)
        self.assertEqual(schedule_number(), 16)
        self.assertEqual(emails_sent_number(), 2)
        student_email = get_mail(0)
        self.assertEqual(student_email.to, [self.data["email"]])
        self.assertEqual(
            student_email.subject,
            f"Potwierdzenie rezerwacji lekcji {self.lesson_2.title}",
        )
        lecturer_reservation_email = get_mail(1)
        self.assertEqual(
            lecturer_reservation_email.to,
            [get_schedule(self.schedules[2].id).lecturer.profile.user.email],
        )
        self.assertEqual(
            lecturer_reservation_email.subject,
            f"Nowy zapis na lekcję {self.lesson_2.title}",
        )

    def test_create_reservation_authenticated_first_reservation_multiple_slot(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_1.id,
            "schedule": self.schedules[3].id,
            "purchase": self.purchase_1.id,
        }
        response = self.client.post(self.endpoint, data)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reservation_number(), 7)
        self.assertEqual(data["lesson"], self.lesson_1.id)
        self.assertNotEqual(data["schedule"], self.schedules[3].id)
        self.assertEqual(get_schedule(data["schedule"]).lesson, self.lesson_1)
        self.assertEqual(schedule_number(), 14)
        self.assertEqual(emails_sent_number(), 2)
        student_email = get_mail(0)
        self.assertEqual(student_email.to, [self.data["email"]])
        self.assertEqual(
            student_email.subject,
            f"Potwierdzenie rezerwacji lekcji {self.lesson_1.title}",
        )
        lecturer_reservation_email = get_mail(1)
        self.assertEqual(
            lecturer_reservation_email.to,
            [
                get_schedule(
                    self.schedules[len(self.schedules) - 1].id
                ).lecturer.profile.user.email
            ],
        )
        self.assertEqual(
            lecturer_reservation_email.subject,
            f"Nowy zapis na lekcję {self.lesson_1.title}",
        )

    def test_create_reservation_authenticated_other_reservation_multiple_slot(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_1.id,
            "schedule": self.long_timeslot_2.id,
            "purchase": self.purchase_1.id,
        }
        response = self.client.post(self.endpoint, data)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reservation_number(), 7)
        self.assertEqual(data["lesson"], self.lesson_1.id)
        self.assertEqual(data["schedule"], self.long_timeslot_2.id)
        self.assertEqual(get_schedule(data["schedule"]).lesson, self.lesson_1)
        self.assertEqual(schedule_number(), 16)
        self.assertEqual(emails_sent_number(), 2)
        student_email = get_mail(0)
        self.assertEqual(student_email.to, [self.data["email"]])
        self.assertEqual(
            student_email.subject,
            f"Potwierdzenie rezerwacji lekcji {self.lesson_1.title}",
        )
        lecturer_reservation_email = get_mail(1)
        self.assertEqual(
            lecturer_reservation_email.to,
            [get_schedule(self.long_timeslot_2.id).lecturer.profile.user.email],
        )
        self.assertEqual(
            lecturer_reservation_email.subject,
            f"Nowy zapis na lekcję {self.lesson_1.title}",
        )

    def test_delete_reservation_unauthenticated(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # delete data
        response = self.client.delete(f"{self.endpoint}/{self.reservation_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reservation_number(), 6)
        self.assertTrue(is_reservation_found(self.reservation_1.id))
        self.assertEqual(emails_sent_number(), 0)

    def test_delete_reservation_authenticated_cancellation(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete data
        response = self.client.delete(f"{self.endpoint}/{self.reservation_1.id}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reservation_number(), 6)
        self.assertTrue(is_reservation_found(self.reservation_1.id))
        self.assertEqual(emails_sent_number(), 0)

    def test_delete_reservation_authenticated_shared(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete data
        self.reservation_1.schedule.start_time = make_aware(
            datetime.now().replace(minute=30, second=0, microsecond=0)
            + timedelta(minutes=30 * 250)
        )
        self.reservation_1.schedule.end_time = make_aware(
            datetime.now().replace(minute=30, second=0, microsecond=0)
            + timedelta(minutes=30 * 251)
        )
        self.reservation_1.schedule.save()

        response = self.client.delete(f"{self.endpoint}/{self.reservation_1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(reservation_number(), 5)
        self.assertFalse(is_reservation_found(self.reservation_1.id))
        self.assertEqual(
            get_schedule(self.reservation_1.schedule.id).lesson,
            self.reservation_1.lesson,
        )
        self.assertEqual(schedule_number(), 16)
        self.assertEqual(emails_sent_number(), 1)
        student_email = get_mail(0)
        self.assertEqual(student_email.to, [self.data["email"]])
        self.assertEqual(
            student_email.subject,
            "Potwierdzenie odwołania rezerwacji",
        )

    def test_delete_reservation_authenticated_not_shared_single_slot(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete data
        self.reservation_4.schedule.start_time = make_aware(
            datetime.now().replace(minute=30, second=0, microsecond=0)
            + timedelta(minutes=30 * 250)
        )
        self.reservation_4.schedule.end_time = make_aware(
            datetime.now().replace(minute=30, second=0, microsecond=0)
            + timedelta(minutes=30 * 251)
        )
        self.reservation_4.schedule.save()

        response = self.client.delete(f"{self.endpoint}/{self.reservation_4.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(reservation_number(), 5)
        self.assertFalse(is_reservation_found(self.reservation_4.id))
        self.assertEqual(get_schedule(self.reservation_4.schedule.id).lesson, None)
        self.assertEqual(schedule_number(), 16)
        self.assertEqual(emails_sent_number(), 1)
        student_email = get_mail(0)
        self.assertEqual(student_email.to, [self.data["email"]])
        self.assertEqual(
            student_email.subject,
            "Potwierdzenie odwołania rezerwacji",
        )

    def test_delete_reservation_authenticated_not_shared_multi_slot(self):
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete data
        lecturer = get_schedule(self.reservation_6.schedule.id).lecturer
        response = self.client.delete(f"{self.endpoint}/{self.reservation_6.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(reservation_number(), 5)
        self.assertFalse(is_reservation_found(self.reservation_6.id))
        self.assertFalse(is_schedule_found(self.reservation_6.schedule.id))
        self.assertEqual(schedule_number(), 18)
        self.assertEqual(emails_sent_number(), 1)
        student_email = get_mail(0)
        self.assertEqual(student_email.to, [self.data["email"]])
        self.assertEqual(
            student_email.subject,
            "Potwierdzenie odwołania rezerwacji",
        )


class ReservationConfirmationTest(TestCase):
    def setUp(self):
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
        self.user_3 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="user3@example.com",
            password="TestPassword123",
            is_active=True,
        )
        self.profile = create_student_profile(profile=create_profile(user=self.user))
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
        for i in range(-10, 50):
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
        create_reservation(
            student=self.profile_2,
            lesson=self.lesson_1,
            schedule=self.schedules[len(self.schedules) - 3],
            purchase=self.purchase_1,
        )
        create_reservation(
            student=self.profile_3,
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
        )
        create_reservation(
            student=self.profile,
            lesson=self.lesson_2,
            schedule=self.schedules[0],
            purchase=self.purchase_2,
        )
        self.schedules[0].lesson = self.lesson_2
        self.schedules[0].save()

    def test_reservation_confirmation(self):
        self.assertEqual(reservation_number(), 4)
        confirm_reservations()
        self.assertEqual(reservation_number(), 3)
        self.assertEqual(emails_sent_number(), 6)
        email = get_mail(0)
        self.assertEqual(email.to, [self.profile.profile.user.email])
        self.assertEqual(email.subject, "Brak realizacji szkolenia")
        email = get_mail(1)
        self.assertEqual(email.to, [self.lecturer_profile.profile.user.email])
        self.assertEqual(email.subject, "Brak realizacji szkolenia")
        email = get_mail(2)
        self.assertEqual(email.to, [self.profile.profile.user.email])
        self.assertEqual(email.subject, "Potwierdzenie realizacji szkolenia")
        email = get_mail(3)
        self.assertEqual(email.to, [self.profile_2.profile.user.email])
        self.assertEqual(email.subject, "Potwierdzenie realizacji szkolenia")
        email = get_mail(4)
        self.assertEqual(email.to, [self.profile_3.profile.user.email])
        self.assertEqual(email.subject, "Potwierdzenie realizacji szkolenia")
        email = get_mail(5)
        self.assertEqual(email.to, [self.lecturer_profile.profile.user.email])
        self.assertEqual(email.subject, "Potwierdzenie realizacji szkolenia")

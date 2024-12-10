from rest_framework import status
from rest_framework.test import APIClient
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
    create_tag,
    create_topic,
    create_candidate,
    create_purchase,
    create_schedule,
    create_teaching,
    create_reservation,
    create_meeting,
    create_module,
    create_finance,
    create_payment,
)
from .helpers import (
    login,
    get_schedule,
    schedule_number,
    is_schedule_found,
    reservation_number,
    is_reservation_found,
    mock_send_message,
    mock_create_event,
    mock_update_event,
    mock_get_recordings,
    mock_set_permissions,
    notifications_number,
    recordings_number,
)
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from reservation.utils import confirm_reservations, pull_recordings
from utils.google.gmail import GmailApi
from utils.google.calendar import CalendarApi
from utils.google.drive import DriveApi


class ReservationTest(TestCase):
    def setUp(self):
        self.endpoint = "/api/reservation"
        self.client = APIClient()
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

        self.candidate_1 = create_candidate(name="No tech knowledge")
        self.candidate_2 = create_candidate(name="Tech interested")

        self.tag_1 = create_tag(name="coding")
        self.tag_2 = create_tag(name="IDE")

        self.module_1 = create_module(
            title="Module 1", lessons=[self.lesson_1, self.lesson_2]
        )
        self.module_2 = create_module(
            title="Module 2", lessons=[self.lesson_3, self.lesson_4]
        )

        self.course = create_course(
            title="course_title",
            description="course_description",
            overview="course_overview",
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
            modules=[self.module_1, self.module_2],
        )

        for module in self.course.modules.all():
            for lesson in module.lessons.all():
                create_teaching(
                    lecturer=self.lecturer_profile,
                    lesson=lesson,
                )

        self.schedules = []
        for i in range(7):
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

        self.later_timeslot = create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=0, second=0, microsecond=0)
                + timedelta(hours=48)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(hours=48)
            ),
        )
        create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(hours=48)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=0, second=0, microsecond=0)
                + timedelta(hours=49)
            ),
        )
        create_schedule(
            lecturer=self.lecturer_profile,
            start_time=make_aware(
                datetime.now().replace(minute=0, second=0, microsecond=0)
                + timedelta(hours=49)
            ),
            end_time=make_aware(
                datetime.now().replace(minute=30, second=0, microsecond=0)
                + timedelta(hours=49)
            ),
        )

        self.purchase_1 = create_purchase(
            lesson=self.lesson_1,
            student=self.profile_1,
            price=self.lesson_1.price,
            payment=create_payment(amount=self.lesson_1.price),
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
            payment=create_payment(amount=self.lesson_2.price),
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
            payment=create_payment(amount=self.lesson_1.price),
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
            payment=create_payment(amount=self.lesson_2.price),
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
            payment=create_payment(amount=self.lesson_2.price),
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
            payment=create_payment(amount=self.lesson_4.price),
        )
        self.reservation_6 = create_reservation(
            student=self.profile_1,
            lesson=self.lesson_4,
            schedule=self.long_timeslot_3,
            purchase=self.purchase_6,
        )
        self.long_timeslot_3.lesson = self.lesson_4
        self.long_timeslot_3.save()

    @patch.object(GmailApi, "_send_message")
    def test_create_reservation_unauthenticated(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
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
        self.assertEqual(_send_message_mock.call_count, 0)

    @patch.object(GmailApi, "_send_message")
    def test_create_reservation_authenticated_not_purchased(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_3.id,
            "schedule": self.schedules[2].id,
            "purchase": self.purchase_1.id,
        }
        response = self.client.post(self.endpoint, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reservation_number(), 6)
        self.assertEqual(_send_message_mock.call_count, 0)

    @patch.object(GmailApi, "_send_message")
    def test_create_reservation_authenticated_time_not_available(
        self, _send_message_mock
    ):
        mock_send_message(mock=_send_message_mock)
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
        self.assertEqual(_send_message_mock.call_count, 0)

    @patch.object(GmailApi, "_send_message")
    def test_create_reservation_authenticated_first_reservation_single_slot(
        self, _send_message_mock
    ):
        mock_send_message(mock=_send_message_mock)
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
        self.assertEqual(_send_message_mock.call_count, 1)
        self.assertEqual(notifications_number(), 1)

    @patch.object(GmailApi, "_send_message")
    @patch.object(CalendarApi, "update")
    def test_create_reservation_authenticated_other_reservation_single_slot(
        self, update_event_mock, _send_message_mock
    ):
        mock_update_event(mock=update_event_mock)
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        meeting = create_meeting(event_id="test_event", url="https://example.com")
        self.schedules[2].meeting = meeting
        self.schedules[2].lesson = self.lesson_2
        self.schedules[2].save()
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
        self.assertEqual(_send_message_mock.call_count, 2)
        self.assertEqual(update_event_mock.call_count, 1)
        self.assertEqual(notifications_number(), 2)

    @patch.object(GmailApi, "_send_message")
    def test_create_reservation_authenticated_first_reservation_multiple_slot(
        self, _send_message_mock
    ):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        data = {
            "lesson": self.lesson_1.id,
            "schedule": self.later_timeslot.id,
            "purchase": self.purchase_1.id,
        }
        response = self.client.post(self.endpoint, data)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reservation_number(), 7)
        self.assertEqual(data["lesson"], self.lesson_1.id)
        self.assertNotEqual(data["schedule"], self.later_timeslot.id)
        self.assertEqual(get_schedule(data["schedule"]).lesson, self.lesson_1)
        self.assertEqual(schedule_number(), 14)
        self.assertEqual(_send_message_mock.call_count, 1)
        self.assertEqual(notifications_number(), 1)

    @patch.object(GmailApi, "_send_message")
    @patch.object(CalendarApi, "update")
    def test_create_reservation_authenticated_other_reservation_multiple_slot(
        self, update_event_mock, _send_message_mock
    ):
        mock_update_event(mock=update_event_mock)
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # post data
        meeting = create_meeting(event_id="test_event", url="https://example.com")
        self.long_timeslot_2.meeting = meeting
        self.long_timeslot_2.lesson = self.lesson_1
        self.long_timeslot_2.save()
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
        self.assertEqual(_send_message_mock.call_count, 2)
        self.assertEqual(update_event_mock.call_count, 1)
        self.assertEqual(notifications_number(), 2)

    @patch.object(GmailApi, "_send_message")
    def test_delete_reservation_unauthenticated(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # delete data
        response = self.client.delete(f"{self.endpoint}/{self.reservation_1.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reservation_number(), 6)
        self.assertTrue(is_reservation_found(self.reservation_1.id))
        self.assertEqual(_send_message_mock.call_count, 0)

    @patch.object(GmailApi, "_send_message")
    def test_delete_reservation_authenticated_cancellation(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
        # login
        login(self, self.data["email"], self.data["password"])
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        # delete data
        response = self.client.delete(f"{self.endpoint}/{self.reservation_1.id}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(reservation_number(), 6)
        self.assertTrue(is_reservation_found(self.reservation_1.id))
        self.assertEqual(_send_message_mock.call_count, 0)

    @patch.object(GmailApi, "_send_message")
    def test_delete_reservation_authenticated_shared(self, _send_message_mock):
        mock_send_message(mock=_send_message_mock)
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
        self.assertEqual(_send_message_mock.call_count, 0)
        self.assertEqual(notifications_number(), 0)

    @patch.object(GmailApi, "_send_message")
    def test_delete_reservation_authenticated_not_shared_single_slot(
        self, _send_message_mock
    ):
        mock_send_message(mock=_send_message_mock)
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
        self.assertEqual(_send_message_mock.call_count, 0)
        self.assertEqual(notifications_number(), 0)

    @patch.object(GmailApi, "_send_message")
    def test_delete_reservation_authenticated_not_shared_multi_slot(
        self, _send_message_mock
    ):
        mock_send_message(mock=_send_message_mock)
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
        self.assertEqual(_send_message_mock.call_count, 0)
        self.assertEqual(notifications_number(), 0)


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
        create_finance(lecturer=self.lecturer_profile, rate=100, commission=0)

        self.technology_1 = create_technology(name="Python")
        self.technology_2 = create_technology(name="JS")
        self.technology_3 = create_technology(name="VBA")

        # course 1
        self.lesson_1 = create_lesson(
            title="Python lesson 1",
            description="bbbb",
            duration="90",
            github_url="https://github.com/loopedupl/lesson",
            price="109.99",
            technologies=[self.technology_1],
        )
        self.lesson_2 = create_lesson(
            title="Python lesson 2",
            description="bbbb",
            duration="30",
            github_url="https://github.com/loopedupl/lesson",
            price="52.99",
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
            payment=create_payment(amount=self.lesson_1.price),
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

    @patch.object(GmailApi, "_send_message")
    @patch.object(CalendarApi, "create")
    def test_reservation_confirmation(self, create_event_mock, _send_message_mock):
        mock_create_event(mock=create_event_mock)
        mock_send_message(mock=_send_message_mock)
        self.assertEqual(reservation_number(), 4)
        confirm_reservations()
        self.assertEqual(reservation_number(), 3)
        self.assertEqual(_send_message_mock.call_count, 6)
        self.assertEqual(create_event_mock.call_count, 1)
        self.assertEqual(notifications_number(), 6)


class RecordingsTest(TestCase):
    def setUp(self):
        self.lecturer_user = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password="Password124!",
            is_active=True,
        )
        self.lecturer_profile = create_lecturer_profile(
            profile=create_profile(user=self.lecturer_user, user_type="W")
        )

        self.schedules = [
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
            for i in range(10)
        ]

    @patch.object(DriveApi, "set_permissions")
    @patch.object(DriveApi, "get_recordings")
    def test_pull_recordings_1(self, get_recordings_mock, set_permissions_mock):
        schedule_ids = [schedule.id for schedule in self.schedules]
        mock_get_recordings(mock=get_recordings_mock, schedule_ids=schedule_ids)
        mock_set_permissions(mock=set_permissions_mock)
        self.assertEqual(recordings_number(), 0)
        pull_recordings()
        self.assertEqual(recordings_number(), len(schedule_ids))
        self.assertEqual(get_recordings_mock.call_count, 1)
        self.assertEqual(set_permissions_mock.call_count, len(schedule_ids))

    @patch.object(DriveApi, "set_permissions")
    @patch.object(DriveApi, "get_recordings")
    def test_pull_recordings_2(self, get_recordings_mock, set_permissions_mock):
        schedule_ids = []
        mock_get_recordings(mock=get_recordings_mock, schedule_ids=schedule_ids)
        mock_set_permissions(mock=set_permissions_mock)
        self.assertEqual(recordings_number(), 0)
        pull_recordings()
        self.assertEqual(recordings_number(), len(schedule_ids))
        self.assertEqual(get_recordings_mock.call_count, 1)
        self.assertEqual(set_permissions_mock.call_count, len(schedule_ids))

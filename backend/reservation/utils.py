from reservation.models import Reservation
from schedule.models import Schedule, Meeting
from schedule.utils import MeetingManager
from django.db.models import F
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from pytz import timezone, utc
from mailer.mailer import Mailer
from const import CANCELLATION_TIME, MINIMUM_STUDENTS_REQUIRED
from notification.utils import notify
import urllib.parse


def confirm_reservations():
    mailer = Mailer()
    now = make_aware(datetime.now())

    schedules = (
        Schedule.objects.filter(lesson__isnull=False, meeting__url__isnull=True)
        .annotate(diff=now - F("start_time"))
        .filter(diff__gte=-timedelta(hours=CANCELLATION_TIME))
    )

    for schedule in schedules:
        reservations = Reservation.objects.filter(schedule=schedule)

        is_lesson_success = reservations.count() >= MINIMUM_STUDENTS_REQUIRED

        if is_lesson_success:
            # create meeting
            meeting_manager = MeetingManager(
                lecturer_email=schedule.lecturer.profile.user.email
            )
            event = meeting_manager.create(
                title=schedule.lesson.title,
                description=schedule.lesson.description,
                start_time=schedule.start_time,
                end_time=schedule.end_time,
                lecturer=schedule.lecturer,
                students=[reservation.student for reservation in reservations],
            )
            meeting = Meeting.objects.create(
                event_id=event["id"], url=event["hangoutLink"]
            )
            schedule.meeting = meeting

        start_time = (
            schedule.start_time.replace(tzinfo=utc)
            .astimezone(timezone("Europe/Warsaw"))
            .strftime("%d-%m-%Y %H:%M")
        )
        lecturer_full_name = f"{schedule.lecturer.profile.user.first_name} {schedule.lecturer.profile.user.last_name}"
        data = {
            **{
                "lesson_title": schedule.lesson.title,
                "lecturer_full_name": lecturer_full_name,
                "lesson_start_time": start_time,
            }
        }

        # send email
        for reservation in reservations:
            if is_lesson_success:
                data = {
                    **data,
                    "meeting_url": schedule.meeting.url,
                }
                mailer.send(
                    email_template="lesson_success.html",
                    to=[reservation.student.profile.user.email],
                    subject="Potwierdzenie realizacji szkolenia",
                    data=data,
                )
                notify(
                    profile=reservation.student.profile,
                    title="Potwierdzenie realizacji szkolenia",
                    subtitle=schedule.lesson.title,
                    description=f"Udało się! Potwierdzamy realizację lekcji, która odbędzie się {start_time} (PL) i będzie prowadzona przez {lecturer_full_name}.",
                    path=f"/account/lessons?sort_by=-created_at&page_size=10&lesson_title={urllib.parse.quote_plus(schedule.lesson.title)}",
                    icon="mdi:school",
                )
            else:
                mailer.send(
                    email_template="lesson_failure.html",
                    to=[reservation.student.profile.user.email],
                    subject="Brak realizacji szkolenia",
                    data=data,
                )
                notify(
                    profile=reservation.student.profile,
                    title="Brak realizacji szkolenia",
                    subtitle=schedule.lesson.title,
                    description=f"Niestety, nie udało się zrealizować lekcję, która planowo odbyłaby się {start_time} (PL) i byłaby prowadzona przez {lecturer_full_name} z powodu niewystarczającej ilości zapisów.",
                    path=f"/account/lessons?sort_by=-created_at&page_size=10&lesson_title={urllib.parse.quote_plus(schedule.lesson.title)}",
                    icon="mdi:school",
                )

        if is_lesson_success:
            mailer.send(
                email_template="lesson_success.html",
                to=[schedule.lecturer.profile.user.email],
                subject="Potwierdzenie realizacji szkolenia",
                data=data,
            )
            notify(
                profile=schedule.lecturer.profile,
                title="Potwierdzenie realizacji szkolenia",
                subtitle=schedule.lesson.title,
                description=f"Udało się! Potwierdzamy realizację lekcji, która odbędzie się {start_time} (PL).",
                path=f"/account/teacher/calendar?time_from={schedule.start_time.strftime('%Y-%m-%d')}&view=day",
                icon="mdi:school",
            )
        else:
            mailer.send(
                email_template="lesson_failure.html",
                to=[schedule.lecturer.profile.user.email],
                subject="Brak realizacji szkolenia",
                data=data,
            )
            notify(
                profile=schedule.lecturer.profile,
                title="Brak realizacji szkolenia",
                subtitle=schedule.lesson.title,
                description=f"Niestety, nie udało się zrealizować lekcję, która planowo odbyłaby się {start_time} (PL) z powodu niewystarczającej ilości zapisów.",
                path=f"/account/teacher/calendar?time_from={schedule.start_time.strftime('%Y-%m-%d')}&view=day",
                icon="mdi:school",
            )
            schedule.lesson = None
            reservations.delete()

        schedule.save()

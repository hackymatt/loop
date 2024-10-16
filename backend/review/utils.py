from reservation.models import Reservation
from schedule.models import Schedule
from review.models import Review
from profile.models import LecturerProfile
from django.db.models import F, Prefetch
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from pytz import timezone, utc
from mailer.mailer import Mailer
from config_global import REMINDER_TIME
from notification.utils import notify
from urllib.parse import quote_plus


def remind_review():
    mailer = Mailer()
    now = make_aware(datetime.now())

    schedules = (
        Schedule.objects.filter(lesson__isnull=False, meeting__url__isnull=False)
        .annotate(diff=now - F("end_time"))
        .filter(
            diff__lte=timedelta(hours=REMINDER_TIME * 2),
            diff__gt=timedelta(hours=REMINDER_TIME),
        )
        .prefetch_related(Prefetch("lecturer", queryset=LecturerProfile.objects.all()))
    )

    reservations = Reservation.objects.filter(schedule__in=schedules).select_related(
        "student", "lesson"
    )

    reservation_dict = {}
    for reservation in reservations:
        reservation_dict.setdefault(reservation.schedule.id, []).append(reservation)

    for schedule in schedules:
        for reservation in reservation_dict.get(schedule.id, []):
            student = reservation.student
            lesson = reservation.lesson

            review_exists = Review.objects.filter(
                student=student, lesson=lesson, lecturer=schedule.lecturer
            ).exists()

            if not review_exists:
                start_time = (
                    schedule.start_time.replace(tzinfo=utc)
                    .astimezone(timezone("Europe/Warsaw"))
                    .strftime("%d-%m-%Y %H:%M")
                )
                lecturer_full_name = schedule.lecturer.full_name

                data = {
                    "lesson_title": schedule.lesson.title,
                    "lecturer_full_name": lecturer_full_name,
                    "lesson_start_time": start_time,
                }

                mailer.send(
                    email_template="review_reminder.html",
                    to=[student.profile.user.email],
                    subject="Prośba o ocenę szkolenia",
                    data=data,
                )

                notify(
                    profile=student.profile,
                    title="Prośba o ocenę szkolenia",
                    subtitle=schedule.lesson.title,
                    description=(
                        f"Proszę daj nam znać jak nam poszło. "
                        f"Dodaj recenzję lekcji, która odbyła się {start_time} (PL) "
                        f"i była prowadzona przez {lecturer_full_name}."
                    ),
                    path=(
                        f"/account/reviews?review_status_exclude=brak&page_size=10&"
                        f"lesson_title={quote_plus(schedule.lesson.title)}"
                    ),
                    icon="mdi:rate-review",
                )

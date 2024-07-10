from reservation.models import Reservation
from schedule.models import Schedule
from django.db.models import F
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from pytz import timezone, utc
from mailer.mailer import Mailer
from const import CANCELLATION_TIME, MINIMUM_STUDENTS_REQUIRED


def confirm_reservations():
    mailer = Mailer()
    now = make_aware(datetime.now())

    schedules = (
        Schedule.objects.filter(lesson__isnull=False, meeting_url__isnull=True)
        .annotate(diff=now - F("start_time"))
        .filter(diff__gte=-timedelta(hours=CANCELLATION_TIME))
    )

    for schedule in schedules:
        reservations = Reservation.objects.filter(schedule=schedule)

        is_lesson_success = reservations.count() >= MINIMUM_STUDENTS_REQUIRED

        if is_lesson_success:
            # create meeting url
            meeting_url = "https://www.google.com"
            schedule.meeting_url = meeting_url

        data = {
            **{
                "lesson_title": schedule.lesson.title,
                "lecturer_full_name": f"{schedule.lecturer.profile.user.first_name} {schedule.lecturer.profile.user.last_name}",
                "lesson_start_time": schedule.start_time.replace(tzinfo=utc)
                .astimezone(timezone("Europe/Warsaw"))
                .strftime("%d-%m-%Y %H:%M"),
                "meeting_url": schedule.meeting_url,
            }
        }

        # send email
        for reservation in reservations:
            if is_lesson_success:
                mailer.send(
                    email_template="lesson_success.html",
                    to=[reservation.student.profile.user.email],
                    subject="Potwierdzenie realizacji szkolenia",
                    data=data,
                )
            else:
                mailer.send(
                    email_template="lesson_failure.html",
                    to=[reservation.student.profile.user.email],
                    subject="Brak realizacji szkolenia",
                    data=data,
                )

        if is_lesson_success:
            mailer.send(
                email_template="lesson_success.html",
                to=[schedule.lecturer.profile.user.email],
                subject="Potwierdzenie realizacji szkolenia",
                data=data,
            )
        else:
            mailer.send(
                email_template="lesson_failure.html",
                to=[schedule.lecturer.profile.user.email],
                subject="Brak realizacji szkolenia",
                data=data,
            )
            schedule.lesson = None
            reservations.delete()

        schedule.save()

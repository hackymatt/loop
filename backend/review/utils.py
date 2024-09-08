from reservation.models import Reservation
from schedule.models import Schedule
from review.models import Review
from django.db.models import F
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from pytz import timezone, utc
from mailer.mailer import Mailer
from const import REMINDER_TIME


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
    )

    for schedule in schedules:
        reservations = Reservation.objects.filter(schedule=schedule)

        for reservation in reservations:
            student = reservation.student
            lesson = reservation.lesson

            review = Review.objects.filter(
                student=student, lesson=lesson, lecturer=schedule.lecturer
            )

            if not review.exists():
                # send reminder
                data = {
                    **{
                        "lesson_title": schedule.lesson.title,
                        "lecturer_full_name": f"{schedule.lecturer.profile.user.first_name} {schedule.lecturer.profile.user.last_name}",
                        "lesson_start_time": schedule.start_time.replace(tzinfo=utc)
                        .astimezone(timezone("Europe/Warsaw"))
                        .strftime("%d-%m-%Y %H:%M"),
                    }
                }
                mailer.send(
                    email_template="review_reminder.html",
                    to=[reservation.student.profile.user.email],
                    subject="Prośba o ocenę szkolenia",
                    data=data,
                )

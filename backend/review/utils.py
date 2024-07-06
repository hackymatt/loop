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

    schedules = Schedule.objects.filter(
        lesson__isnull=False, meeting_url__isnull=False
    ).annotate(diff=now - F("end_time"))

    for schedule in schedules:
        print(now)
        print(schedule.end_time)
        print(schedule.diff)

    schedules = schedules.filter(
        diff__lte=timedelta(minutes=REMINDER_TIME * 60),
        diff__gt=timedelta(minutes=(REMINDER_TIME - 0.5) * 60),
    )

    for schedule in schedules:
        print(schedule.end_time)
        print(schedule.diff)
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
                        "lecturer_full_name": f"{schedule.lecturer.user.first_name} {schedule.lecturer.user.last_name}",
                        "lesson_start_time": schedule.start_time.replace(tzinfo=utc)
                        .astimezone(timezone("Europe/Warsaw"))
                        .strftime("%d-%m-%Y %H:%M"),
                    }
                }
                mailer.send(
                    email_template="review_reminder.html",
                    to=[reservation.student.user.email],
                    subject="Prośba o ocenę szkolenia",
                    data=data,
                )

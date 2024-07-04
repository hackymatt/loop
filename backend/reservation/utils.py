from .models import Reservation
from schedule.models import Schedule
from django.db.models import F
from django.db.models.functions import ExtractSecond
from datetime import datetime
from django.utils.timezone import make_aware
from pytz import timezone, utc
from mailer.mailer import Mailer
from const import CANCELLATION_TIME, MINIMUM_STUDENTS_REQUIRED


def confirm_reservations():
    schedules = (
        Schedule.objects.filter(lesson__isnull=False, meeting_url__isnull=True)
        .annotate(diff=ExtractSecond(make_aware(datetime.now()) - F("start_time")))
        .filter(diff__gte=-CANCELLATION_TIME * 60 * 60)
    )
    for schedule in schedules:
        # create meeting url
        meeting_url = ""
        schedule.meeting_url = meeting_url

        reservations = Reservation.objects.filter(schedule=schedule)
        if reservations.count() >= MINIMUM_STUDENTS_REQUIRED:
            # send confirmation email
            for reservation in reservations:
                mailer = Mailer()
                data = {
                    **{
                        "lesson_title": reservation.lesson.title,
                        "lecturer_full_name": f"{schedule.lecturer.user.first_name} {schedule.lecturer.user.last_name}",
                        "lesson_start_time": schedule.start_time.replace(tzinfo=utc)
                        .astimezone(timezone("Europe/Warsaw"))
                        .strftime("%d-%m-%Y %H:%M"),
                    }
                }
                mailer.send(
                    email_template="lesson_confirmation.html",
                    to=[reservation.student.user.email],
                    subject="Potwierdzenie realizacji szkolenia",
                    data=data,
                )
        else:
            # remove reservations
            schedule.lesson = None
            reservations.delete()

        schedule.save()

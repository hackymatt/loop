from reservation.models import Reservation
from schedule.models import Schedule, Meeting, Recording
from profile.models import StudentProfile, LecturerProfile
from schedule.utils import MeetingManager, get_min_students_required
from django.db.models import F, Prefetch
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from pytz import timezone, utc
from mailer.mailer import Mailer
from config_global import CANCELLATION_TIME
from notification.utils import notify
from urllib.parse import quote_plus
from utils.google.drive import DriveApi
import re
from utils.logger.logger import logger


def get_meeting_title(schedule: Schedule):
    meeting_id = "{:07d}".format(schedule.id)
    return f"{schedule.lesson.title} #{meeting_id}#"


def confirm_reservations():
    mailer = Mailer()
    now = make_aware(datetime.now())

    schedules = (
        Schedule.objects.filter(lesson__isnull=False, meeting__url__isnull=True)
        .add_diff()
        .filter(diff__gte=-timedelta(hours=CANCELLATION_TIME))
        .prefetch_related(
            Prefetch("lecturer", queryset=LecturerProfile.objects.add_full_name())
        )
    )

    def send_lesson_email_and_notify(reservations, is_success, schedule, data):
        email_template = "lesson_success.html" if is_success else "lesson_failure.html"
        subject = (
            "Potwierdzenie realizacji szkolenia"
            if is_success
            else "Brak realizacji szkolenia"
        )
        icon = "mdi:school"

        for reservation in reservations:
            mailer.send(
                email_template=email_template,
                to=[reservation.student.profile.user.email],
                subject=subject,
                data=data,
            )
            notify(
                profile=reservation.student.profile,
                title=subject,
                subtitle=schedule.lesson.title,
                description=data["description"],
                path=f"/account/lessons?sort_by=-created_at&page_size=10&lesson_title={quote_plus(schedule.lesson.title)}",
                icon=icon,
            )

    def send_lecturer_email_and_notify(schedule, is_success, data):
        email_template = "lesson_success.html" if is_success else "lesson_failure.html"
        subject = (
            "Potwierdzenie realizacji szkolenia"
            if is_success
            else "Brak realizacji szkolenia"
        )
        icon = "mdi:school"

        mailer.send(
            email_template=email_template,
            to=[schedule.lecturer.profile.user.email],
            subject=subject,
            data=data,
        )
        notify(
            profile=schedule.lecturer.profile,
            title=subject,
            subtitle=schedule.lesson.title,
            description=data["description"],
            path=f"/account/teacher/calendar?time_from={schedule.start_time.strftime('%Y-%m-%d')}&view=day",
            icon=icon,
        )

    for schedule in schedules:
        reservations = Reservation.objects.filter(schedule=schedule).prefetch_related(
            Prefetch("student", queryset=StudentProfile.objects.add_full_name())
        )

        is_lesson_success = reservations.count() >= get_min_students_required(
            lecturer=schedule.lecturer, lesson=schedule.lesson
        )

        start_time = schedule.start_time.astimezone(timezone("Europe/Warsaw")).strftime(
            "%d-%m-%Y %H:%M"
        )
        lecturer_full_name = schedule.lecturer.full_name
        data = {
            "lesson_title": schedule.lesson.title,
            "lecturer_full_name": lecturer_full_name,
            "lesson_start_time": start_time,
        }

        if is_lesson_success:
            meeting_manager = MeetingManager()
            event = meeting_manager.create(
                title=get_meeting_title(schedule=schedule),
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
            data["meeting_url"] = meeting.url

            data["description"] = (
                "Udało się! Potwierdzamy realizację lekcji, która odbędzie się "
                f"{start_time} (PL) i będzie prowadzona przez {lecturer_full_name}."
            )

            send_lesson_email_and_notify(reservations, True, schedule, data)
            send_lecturer_email_and_notify(schedule, True, data)

        else:
            data["description"] = (
                f"Niestety, nie udało się zrealizować lekcję, która planowo "
                f"odbyłaby się {start_time} (PL) i byłaby prowadzona przez {lecturer_full_name} z powodu "
                "niewystarczającej ilości zapisów."
            )
            send_lesson_email_and_notify(reservations, False, schedule, data)
            send_lecturer_email_and_notify(schedule, False, data)

            schedule.lesson = None
            reservations.delete()

        schedule.save()


def pull_recordings():
    one_hour_ago = (datetime.now(utc) - timedelta(hours=1)).isoformat()

    drive_api = DriveApi()

    recordings = drive_api.get_recordings(
        query=f"modifiedTime >= '{one_hour_ago}' and mimeType='video/mp4'"
    )

    schedule_id_pattern = re.compile(r"#(\d+)#")

    recordings_to_create = []
    for recording in recordings:
        file_id = recording["id"]
        file_name = recording["name"]
        file_url = recording["webContentLink"]

        match = schedule_id_pattern.search(file_name)
        if match:
            schedule_id = match.group(1)
            schedule = Schedule.objects.get(pk=schedule_id)

            drive_api.set_permissions(
                file_id=file_id, permissions={"type": "anyone", "role": "reader"}
            )

            recordings_to_create.append(
                Recording(
                    schedule=schedule,
                    file_id=file_id,
                    file_name=file_name,
                    file_url=file_url,
                )
            )

        else:
            logger.error(
                f"Schedule ID not found in file name {file_name}", exc_info=True
            )

    if recordings_to_create:
        Recording.objects.bulk_create(recordings_to_create)
    else:
        logger.error("No recordings to create", exc_info=True)

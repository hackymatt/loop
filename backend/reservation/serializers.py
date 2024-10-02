from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from reservation.models import Reservation
from profile.models import Profile, StudentProfile
from schedule.models import Schedule
from schedule.utils import MeetingManager
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from pytz import timezone, utc
from mailer.mailer import Mailer
from config_global import LESSON_DURATION_MULTIPLIER, CANCELLATION_TIME
from notification.utils import notify
import urllib.parse


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        exclude = ("student",)

    def check_lesson(self, lesson, purchase):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)

        if not (
            purchase.student == StudentProfile.objects.get(profile=profile)
            and purchase.lesson == lesson
        ):
            raise ValidationError({"lesson": "Lekcja nie została zakupiona."})

        return lesson

    def get_timeslots(self, schedule, lesson):
        duration = lesson.duration
        required_timeslots = duration / LESSON_DURATION_MULTIPLIER
        lecturer = schedule.lecturer
        start_time = schedule.start_time
        end_time = start_time + timedelta(minutes=30 * required_timeslots)

        lecturer_timeslots = Schedule.objects.filter(
            lecturer=lecturer,
            start_time__gte=start_time,
            end_time__lte=end_time,
        ).all()
        timeslots = (
            lecturer_timeslots.filter(
                lesson=lesson,
            ).all()
            | lecturer_timeslots.filter(
                lesson__isnull=True,
            ).all()
        )

        if timeslots.count() == (duration / LESSON_DURATION_MULTIPLIER):
            return timeslots
        elif timeslots.count() == 1 and timeslots.first().lesson == lesson:
            return timeslots
        else:
            return None

    def check_schedule(self, schedule, lesson):
        if not self.get_timeslots(schedule, lesson):
            raise ValidationError({"schedule": "Wybrany termin jest niedostępny."})

        return schedule

    def validate(self, data):
        self.check_lesson(lesson=data["lesson"], purchase=data["purchase"])
        self.check_schedule(schedule=data["schedule"], lesson=data["lesson"])

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)

        schedule = validated_data["schedule"]
        lesson = validated_data["lesson"]
        purchase = validated_data["purchase"]

        timeslots = self.get_timeslots(schedule=schedule, lesson=lesson).order_by(
            "start_time"
        )
        start_time = timeslots.first().start_time
        end_time = timeslots.last().end_time
        lecturer = timeslots.first().lecturer

        if timeslots.count() == 1:
            timeslot = timeslots.first()
            if timeslot.lesson is None:
                timeslot.lesson = lesson
                timeslot.save()
            lesson_schedule = timeslot
        else:
            lesson_schedule, _ = Schedule.objects.get_or_create(
                lecturer=lecturer,
                start_time=start_time,
                end_time=end_time,
                lesson=lesson,
            )
            timeslots.exclude(id=lesson_schedule.id).delete()

        reservation = Reservation.objects.create(
            student=StudentProfile.objects.get(profile=profile),
            lesson=lesson,
            schedule=lesson_schedule,
            purchase=purchase,
        )

        mailer = Mailer()
        reservations = Reservation.objects.filter(schedule=lesson_schedule).all()
        students_count = reservations.count()

        start_time = (
            schedule.start_time.replace(tzinfo=utc)
            .astimezone(timezone("Europe/Warsaw"))
            .strftime("%d-%m-%Y %H:%M")
        )
        lecturer_full_name = f"{schedule.lecturer.profile.user.first_name} {schedule.lecturer.profile.user.last_name}"

        if (schedule.start_time - make_aware(datetime.now())) < timedelta(
            hours=CANCELLATION_TIME
        ):
            meeting_manager = MeetingManager()
            meeting_manager.update(
                event_id=schedule.meeting.event_id,
                title=schedule.lesson.title,
                description=schedule.lesson.description,
                start_time=schedule.start_time,
                end_time=schedule.end_time,
                lecturer=schedule.lecturer,
                students=[reservation.student for reservation in reservations],
            )
            data = {
                **{
                    "lesson_title": schedule.lesson.title,
                    "lecturer_full_name": lecturer_full_name,
                    "lesson_start_time": start_time,
                    "meeting_url": schedule.meeting.url,
                }
            }
            mailer.send(
                email_template="lesson_success.html",
                to=[profile.user.email],
                subject="Potwierdzenie realizacji szkolenia",
                data=data,
            )
            notify(
                profile=profile,
                title="Potwierdzenie realizacji szkolenia",
                subtitle=lesson.title,
                description=f"Udało się! Potwierdzamy realizację lekcji, która odbędzie się {start_time} (PL) i będzie prowadzona przez {lecturer_full_name}.",
                path=f"/account/lessons?sort_by=-created_at&page_size=10&lesson_title={urllib.parse.quote_plus(schedule.lesson.title)}",
                icon="mdi:school",
            )

        # notify lecturer
        student_full_name = f"{profile.user.first_name} {profile.user.last_name}"
        data = {
            **{
                "lesson_title": lesson.title,
                "lesson_start_time": start_time,
                "student_full_name": student_full_name,
                "students_count": students_count,
            }
        }
        mailer.send(
            email_template="new_reservation.html",
            to=[schedule.lecturer.profile.user.email],
            subject=f"Nowy zapis na lekcję {lesson.title}",
            data=data,
        )
        notify(
            profile=schedule.lecturer.profile,
            title="Nowy zapis na lekcję",
            subtitle=lesson.title,
            description=f"Lista potencjalnych uczestników lekcji, która planowo odbędzie się {start_time} (PL) została powiększona o nowy zapis studenta {student_full_name}. Aktualna liczba uczestników: {students_count}.",
            path=f"/account/teacher/calendar?time_from={schedule.start_time.strftime('%Y-%m-%d')}&view=day",
            icon="mdi:invoice-text-new",
        )

        return reservation

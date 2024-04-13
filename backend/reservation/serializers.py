from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ValidationError,
)
from reservation.models import Reservation
from profile.models import Profile
from lesson.models import Lesson, Technology
from purchase.models import Purchase
from schedule.models import Schedule
from datetime import timedelta
from pytz import timezone, utc
from utils.mailer.mailer import Mailer

MIN_LESSON_DURATION_MINS = 30


class ProfileSerializer(ModelSerializer):
    first_name = CharField(source="user.first_name")
    last_name = CharField(source="user.last_name")
    email = EmailField(source="user.email")

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class ScheduleSerializer(ModelSerializer):
    lecturer = ProfileSerializer()

    class Meta:
        model = Schedule
        fields = "__all__"


class ReservationGetSerializer(ModelSerializer):
    lesson = LessonSerializer()
    schedule = ScheduleSerializer()

    class Meta:
        model = Reservation
        fields = (
            "lesson",
            "schedule",
        )


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        exclude = ("student",)

    def check_lesson(self, lesson, purchase):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)

        if not (purchase.student == profile and purchase.lesson == lesson):
            raise ValidationError({"lesson": "Lekcja nie została zakupiona."})

        return lesson

    def get_timeslots(self, schedule, lesson):
        duration = lesson.duration
        required_timeslots = duration / MIN_LESSON_DURATION_MINS
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

        if timeslots.count() == (duration / MIN_LESSON_DURATION_MINS):
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

        previous_students_count = Reservation.objects.filter(
            schedule=lesson_schedule
        ).count()

        reservation = Reservation.objects.create(
            student=profile, lesson=lesson, schedule=lesson_schedule, purchase=purchase
        )

        mailer = Mailer()
        students_count = Reservation.objects.filter(schedule=lesson_schedule).count()

        # notify student
        data = {
            **{
                "lesson_title": lesson.title,
                "lecturer_full_name": f"{schedule.lecturer.user.first_name} {schedule.lecturer.user.last_name}",
                "lesson_start_time": schedule.start_time.replace(tzinfo=utc)
                .astimezone(timezone("Europe/Warsaw"))
                .strftime("%d-%m-%Y %H:%M"),
                "meeting_url": "",
            }
        }
        mailer.send(
            email_template="add_reservation.html",
            to=[profile.user.email],
            subject=f"Potwierdzenie rezerwacji na lekcję {lesson.title}.",
            data=data,
        )

        # notify lecturer
        data = {
            **{
                "lesson_title": lesson.title,
                "lesson_start_time": schedule.start_time.replace(tzinfo=utc)
                .astimezone(timezone("Europe/Warsaw"))
                .strftime("%d-%m-%Y %H:%M"),
                "meeting_url": "",
                "student_full_name": f"{profile.user.first_name} {profile.user.last_name}",
                "students_count": students_count,
            }
        }
        if previous_students_count == 0:
            mailer.send(
                email_template="reserve_timeslot.html",
                to=[schedule.lecturer.user.email],
                subject="Nowa rezerwacja terminu.",
                data=data,
            )

        mailer.send(
            email_template="new_reservation.html",
            to=[schedule.lecturer.user.email],
            subject=f"Nowy zapis na lekcję {lesson.title}.",
            data=data,
        )

        return reservation

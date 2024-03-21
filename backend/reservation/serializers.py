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

    def check_lesson(self, lesson):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)

        if not Purchase.objects.filter(student=profile, lesson=lesson).exists():
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
        self.check_lesson(lesson=data["lesson"])
        self.check_schedule(schedule=data["schedule"], lesson=data["lesson"])

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)

        schedule = validated_data["schedule"]
        lesson = validated_data["lesson"]

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

        return Reservation.objects.create(
            student=profile, lesson=lesson, schedule=lesson_schedule
        )

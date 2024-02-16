from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ValidationError,
)
from reservation.models import Reservation
from profile.models import Profile
from course.models import Course
from lesson.models import Lesson, Technology
from purchase.models import Purchase
from schedule.models import Schedule


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

    def validate_lesson(self, lesson):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)

        if not Purchase.objects.filter(student=profile, lesson=lesson).exists():
            raise ValidationError({"lesson": "Lekcja nie została zakupiona."})

        return lesson

    def validate_schedule(self, schedule):
        if Reservation.objects.filter(schedule=schedule).exists():
            raise ValidationError({"schedule": "Wybrany termin jest niedostępny."})

        return schedule

    def create(self, validated_data):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)
        return Reservation.objects.create(**validated_data, student=profile)

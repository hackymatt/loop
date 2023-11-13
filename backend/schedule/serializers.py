from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    DateTimeField,
    ListField,
)
from course.models import Lesson
from schedule.models import Schedule
from profile.models import Profile


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
            "image",
        )


class ScheduleGetSerializer(ModelSerializer):
    lecturer = ProfileSerializer()

    class Meta:
        model = Schedule
        fields = (
            "lecturer",
            "time",
        )


class ScheduleSerializer(ModelSerializer):
    times = ListField(child=DateTimeField())

    class Meta:
        model = Schedule
        exclude = ("time",)

    def create(self, validated_data):
        lecturer_id = validated_data.pop("lecturer")
        lecturer = Profile.objects.get(pk=lecturer_id)
        lesson_id = validated_data.pop("lesson")
        lesson = Lesson.objects.get(pk=lesson_id)
        times = validated_data.pop("times")

        Schedule.objects.filter(lesson=lesson, lecturer=lecturer).all().delete()
        schedules = Schedule.objects.bulk_create(
            [Schedule(lesson=lesson, lecturer=lecturer, time=time) for time in times]
        )

        return schedules

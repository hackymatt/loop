from rest_framework.serializers import ModelSerializer, SerializerMethodField
from schedule.models import Schedule
from profile.models import Profile
from lesson.models import Lesson
from reservation.models import Reservation
from const import MINIMUM_STUDENTS_REQUIRED


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
        )


class ManageScheduleGetSerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = Schedule
        exclude = (
            "lecturer",
            "modified_at",
            "created_at",
        )


class ManageScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        exclude = (
            "lecturer",
            "lesson",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        lecturer = Profile.objects.get(user=user)

        return Schedule.objects.create(lecturer=lecturer, **validated_data)


class ScheduleSerializer(ModelSerializer):
    students_required = SerializerMethodField("get_students_required")

    class Meta:
        model = Schedule
        exclude = (
            "lesson",
            "lecturer",
            "modified_at",
            "created_at",
        )

    def get_students_required(self, schedule):
        return max(
            MINIMUM_STUDENTS_REQUIRED
            - Reservation.objects.filter(schedule=schedule).count(),
            0,
        )

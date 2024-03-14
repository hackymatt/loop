from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
)
from schedule.models import Schedule
from profile.models import Profile
from lesson.models import Lesson
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


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title", )

class ScheduleGetSerializer(ModelSerializer):
    lesson = LessonSerializer()
    class Meta:
        model = Schedule
        exclude = (
            "lecturer",
            "modified_at",
            "created_at",
        )


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        exclude = ("lecturer","lesson", )

    def create(self, validated_data):
        user = self.context["request"].user
        lecturer = Profile.objects.get(user=user)

        return Schedule.objects.create(lecturer=lecturer, **validated_data)
        

from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    SerializerMethodField,
)
from course.models import Course
from lesson.models import Lesson, Technology
from teaching.models import Teaching
from profile.models import Profile


class TeachingInstanceSerializer(ModelSerializer):
    class Meta:
        model = Teaching
        exclude = (
            "lecturer",
            "lesson",
            "modified_at",
            "created_at",
        )


class TeachingGetSerializer(ModelSerializer):
    teaching = SerializerMethodField("get_teaching")

    class Meta:
        model = Lesson
        exclude = (
            "technologies",
            "description",
            "modified_at",
            "created_at",
        )

    def get_teaching(self, lesson):
        user = self.context["request"].user
        lecturer = Profile.objects.get(user=user)
        teaching = Teaching.objects.filter(lecturer=lecturer, lesson=lesson)

        if teaching.exists():
            return TeachingInstanceSerializer(teaching.first()).data

        return {}


class TeachingSerializer(ModelSerializer):
    class Meta:
        model = Teaching
        exclude = ("lecturer",)

    def create(self, validated_data):
        user = self.context["request"].user
        lecturer = Profile.objects.get(user=user)

        lesson = validated_data.pop("lesson")

        return Teaching.objects.create(lecturer=lecturer, lesson=lesson)

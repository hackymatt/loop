from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField,
)
from drf_extra_fields.fields import Base64ImageField
from lesson.models import Lesson
from teaching.models import Teaching
from profile.models import LecturerProfile


class ManageTeachingGetSerializer(ModelSerializer):
    teaching = SerializerMethodField()
    teaching_id = SerializerMethodField()

    class Meta:
        model = Lesson
        exclude = (
            "technologies",
            "description",
            "modified_at",
            "created_at",
        )

    def get_teaching(self, lesson: Lesson):
        return bool(lesson.teaching_id)

    def get_teaching_id(self, lesson):
        return lesson.teaching_id


class ManageTeachingSerializer(ModelSerializer):
    class Meta:
        model = Teaching
        exclude = ("lecturer",)

    def create(self, validated_data):
        user = self.context["request"].user
        lecturer = LecturerProfile.objects.get(profile__user=user)

        lesson = validated_data.pop("lesson")

        return Teaching.objects.create(lecturer=lecturer, lesson=lesson)


class LecturerSerializer(ModelSerializer):
    gender = CharField(source="profile.gender")
    first_name = CharField(source="profile.user.first_name")
    image = Base64ImageField(source="profile.image")

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "first_name",
            "gender",
            "image",
        )


class TeachingSerializer(ModelSerializer):
    lecturer = LecturerSerializer()

    class Meta:
        model = Teaching
        exclude = (
            "modified_at",
            "created_at",
        )

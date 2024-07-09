from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    UUIDField,
    SerializerMethodField,
)
from drf_extra_fields.fields import Base64ImageField
from lesson.models import Lesson
from teaching.models import Teaching
from profile.models import Profile, LecturerProfile


def get_teaching_instance(self, lesson):
    user = self.context["request"].user
    lecturer = Profile.objects.get(user=user)
    teaching = Teaching.objects.filter(lecturer__profile=lecturer, lesson=lesson)

    return teaching


class ManageTeachingGetSerializer(ModelSerializer):
    teaching = SerializerMethodField("get_teaching")
    teaching_id = SerializerMethodField("get_teaching_id")

    class Meta:
        model = Lesson
        exclude = (
            "technologies",
            "description",
            "modified_at",
            "created_at",
        )

    def get_teaching(self, lesson):
        return get_teaching_instance(self=self, lesson=lesson).exists()

    def get_teaching_id(self, lesson):
        teaching = get_teaching_instance(self=self, lesson=lesson)
        if teaching.exists():
            return teaching.first().id

        return None


class ManageTeachingSerializer(ModelSerializer):
    class Meta:
        model = Teaching
        exclude = ("lecturer",)

    def create(self, validated_data):
        user = self.context["request"].user
        lecturer = LecturerProfile.objects.get(profile=Profile.objects.get(user=user))

        lesson = validated_data.pop("lesson")

        return Teaching.objects.create(lecturer=lecturer, lesson=lesson)


class LecturerSerializer(ModelSerializer):
    uuid = UUIDField(source="profile.uuid")
    gender = CharField(source="profile.get_gender_display")
    first_name = CharField(source="profile.user.first_name")
    email = EmailField(source="profile.user.email")
    image = Base64ImageField(source="profile.image")

    class Meta:
        model = LecturerProfile
        fields = (
            "uuid",
            "first_name",
            "gender",
            "email",
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

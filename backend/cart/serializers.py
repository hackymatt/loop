from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from lesson.models import Lesson, Technology
from cart.models import Cart
from profile.models import Profile, LecturerProfile, StudentProfile


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")

    class Meta:
        model = LecturerProfile
        fields = ("full_name",)

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = (
            "id",
            "modified_at",
            "created_at",
        )


class LessonSerializer(ModelSerializer):
    technologies = SerializerMethodField()
    lecturers = SerializerMethodField()

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "duration",
            "price",
            "technologies",
            "lecturers",
        )

    def get_lecturers(self, lesson: Lesson):
        lecturer_ids = lesson.lecturers_ids
        lecturers = (
            LecturerProfile.objects.add_full_name()
            .add_profile_ready()
            .filter(id__in=lecturer_ids, profile_ready=True)
            .order_by("full_name")
        )
        return LecturerSerializer(
            lecturers, many=True, context={"request": self.context.get("request")}
        ).data

    def get_technologies(self, lesson: Lesson):
        technologies_ids = lesson.technologies_ids
        technologies = Technology.objects.filter(id__in=technologies_ids)
        return TechnologySerializer(technologies, many=True).data


class CartGetSerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = Cart
        exclude = ("student",)


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = ("lesson",)

    def create(self, validated_data):
        user = self.context["request"].user
        student = Profile.objects.get(user=user)

        obj, _ = Cart.objects.get_or_create(
            student=StudentProfile.objects.get(profile=student), **validated_data
        )

        return obj

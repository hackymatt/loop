from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from lesson.models import Lesson, Technology
from cart.models import Cart
from profile.models import Profile
from teaching.models import Teaching
from django.db.models.functions import Concat
from django.db.models import Value


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")

    class Meta:
        model = Profile
        fields = ("full_name",)

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = (
            "id",
            "modified_at",
            "created_at",
        )


class LessonSerializer(ModelSerializer):
    technologies = TechnologySerializer(many=True)
    lecturers = SerializerMethodField("get_lesson_lecturers")

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

    def get_lesson_lecturers(self, lesson):
        lecturer_ids = Teaching.objects.filter(lesson=lesson).values("lecturer")
        lecturers = (
            Profile.objects.filter(id__in=lecturer_ids)
            .annotate(
                full_name=Concat("user__first_name", Value(" "), "user__last_name")
            )
            .order_by("full_name")
        )
        return LecturerSerializer(
            lecturers, many=True, context={"request": self.context.get("request")}
        ).data


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

        obj, _ = Cart.objects.get_or_create(student=student, **validated_data)

        return obj

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from lesson.models import Lesson, Technology
from wishlist.models import Wishlist
from profile.models import Profile, LecturerProfile, StudentProfile
from teaching.models import Teaching
from django.db.models.functions import Concat
from django.db.models import Value, Q


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")

    class Meta:
        model = LecturerProfile
        fields = ("full_name",)

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name


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
            LecturerProfile.objects.exclude(
                Q(title__isnull=True) | Q(description__isnull=True)
            )
            .filter(id__in=lecturer_ids)
            .annotate(
                full_name=Concat(
                    "profile__user__first_name", Value(" "), "profile__user__last_name"
                )
            )
            .order_by("full_name")
        )
        return LecturerSerializer(
            lecturers, many=True, context={"request": self.context.get("request")}
        ).data


class WishlistGetSerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = Wishlist
        exclude = ("student",)


class WishlistSerializer(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ("lesson",)

    def create(self, validated_data):
        user = self.context["request"].user
        student = Profile.objects.get(user=user)

        obj, _ = Wishlist.objects.get_or_create(
            student=StudentProfile.objects.get(profile=student), **validated_data
        )

        return obj

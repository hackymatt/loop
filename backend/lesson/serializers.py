from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ValidationError,
    IntegerField,
    FloatField,
)
from drf_extra_fields.fields import Base64ImageField
from lesson.models import Lesson, LessonPriceHistory
from technology.models import Technology
from profile.models import LecturerProfile
from config_global import LESSON_DURATION_MULTIPLIER, GITHUB_REPO
from notification.utils import notify
from urllib.parse import quote_plus


def notify_lecturer(lesson):
    for lecturer in LecturerProfile.objects.all():
        notify(
            profile=lecturer.profile,
            title="Nowa lekcja w ofercie",
            subtitle=lesson.title,
            description="Właśnie dodaliśmy nową lekcję. Zacznij ją prowadzić.",
            path=f"/account/teacher/teaching/?sort_by=title&page_size=10&title={quote_plus(lesson.title)}",
            icon="mdi:teach",
        )


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image", required=True)

    class Meta:
        model = LecturerProfile
        fields = ("id", "full_name", "gender", "image")

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = ("modified_at", "created_at")


class LessonGetSerializer(ModelSerializer):
    lecturers = SerializerMethodField()
    students_count = IntegerField()
    rating = FloatField()
    rating_count = IntegerField()
    technologies = TechnologySerializer(many=True, source="ordered_technologies")

    class Meta:
        model = Lesson
        exclude = ("created_at", "modified_at")

    def get_lecturers(self, lesson):
        lecturers = (
            LecturerProfile.objects.all()
            .filter(profile_ready=True, id__in=lesson.lecturers_ids)
            .order_by("full_name")
        )
        return LecturerSerializer(
            lecturers, many=True, context={"request": self.context.get("request")}
        ).data


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        exclude = ("created_at", "modified_at")

    def validate_duration(self, duration):
        if duration % LESSON_DURATION_MULTIPLIER != 0:
            raise ValidationError(
                f"Czas lekcji musi być wielokrotnością {LESSON_DURATION_MULTIPLIER} minut."
            )
        return duration

    def validate_github_url(self, github_url):
        if not github_url.startswith(GITHUB_REPO):
            raise ValidationError(f"Github URL musi zaczynać się od {GITHUB_REPO}.")
        return github_url

    def create(self, validated_data):
        technologies = validated_data.pop("technologies", [])
        lesson = Lesson.objects.create(**validated_data)

        if technologies:
            lesson.technologies.set(technologies)

        if lesson.active:
            notify_lecturer(lesson)

        return lesson

    def update(self, instance: Lesson, validated_data):
        technologies = validated_data.pop("technologies", [])
        current_price = instance.price
        new_price = validated_data.get("price", current_price)

        if current_price != new_price:
            LessonPriceHistory.objects.create(lesson=instance, price=current_price)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        instance.technologies.set(technologies)

        if technologies:
            instance.technologies.clear()
            instance.technologies.set(technologies)

        if instance.active:
            notify_lecturer(instance)

        return instance


class LessonPriceHistorySerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = LessonPriceHistory
        exclude = ("modified_at",)

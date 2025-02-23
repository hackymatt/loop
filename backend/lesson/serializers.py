from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ValidationError,
)
from django.db.models import Case, When, IntegerField
from drf_extra_fields.fields import Base64ImageField
from lesson.models import (
    Lesson,
    LessonPriceHistory,
)
from technology.models import Technology
from profile.models import LecturerProfile
from config_global import LESSON_DURATION_MULTIPLIER
from notification.utils import notify
from urllib.parse import quote_plus
from config_global import GITHUB_REPO
from math import ceil


def format_rating(value):
    if value is None:
        return None
    return ceil(value * 10) / 10


def notify_lecturer(lesson: Lesson):
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
    gender = CharField(source="profile.gender")
    image = Base64ImageField(source="profile.image", required=True)

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = (
            "description",
            "modified_at",
            "created_at",
        )


class LessonGetSerializer(ModelSerializer):
    lecturers = SerializerMethodField()
    students_count = SerializerMethodField()
    rating = SerializerMethodField()
    rating_count = SerializerMethodField()
    technologies = SerializerMethodField()

    def get_technologies(self, lesson: Lesson):
        technology_ids = list(
            Lesson.technologies.through.objects.filter(lesson=lesson)
            .order_by("id")
            .values_list("technology_id", flat=True)
        )
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(technology_ids)],
            output_field=IntegerField(),
        )
        technologies = Technology.objects.filter(id__in=technology_ids).order_by(
            preserved_order
        )
        return TechnologySerializer(technologies, many=True).data

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

    def get_rating(self, lesson: Lesson):
        return format_rating(lesson.rating)

    def get_rating_count(self, lesson: Lesson):
        return lesson.rating_count

    def get_students_count(self, lesson: Lesson):
        return lesson.students_count

    class Meta:
        model = Lesson
        exclude = (
            "created_at",
            "modified_at",
        )

class LessonAdminSerializer(ModelSerializer):
    technologies = SerializerMethodField()

    def get_technologies(self, lesson: Lesson):
        technology_ids = list(
            Lesson.technologies.through.objects.filter(lesson=lesson)
            .order_by("id")
            .values_list("technology_id", flat=True)
        )
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(technology_ids)],
            output_field=IntegerField(),
        )
        technologies = Technology.objects.filter(id__in=technology_ids).order_by(
            preserved_order
        )
        return TechnologySerializer(technologies, many=True).data
    class Meta:
        model = Lesson
        exclude = (
            "created_at",
            "modified_at",
        )


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        exclude = (
            "created_at",
            "modified_at",
        )

    def validate_duration(self, duration):
        if duration % LESSON_DURATION_MULTIPLIER != 0:
            raise ValidationError(
                f"Czas lekcji musi być wielokrotnością {LESSON_DURATION_MULTIPLIER} minut."
            )

        return duration

    def validate_github_url(self, github_url):
        if not github_url.startswith(GITHUB_REPO):
            raise ValidationError(
                f"Github url musi być rozpoczynać się na {GITHUB_REPO} minut."
            )

        return github_url

    def add_technology(self, lesson: Lesson, technologies):
        names = [technology.name for technology in technologies]
        existing_names = set(
            Technology.objects.filter(name__in=names).values_list("name", flat=True)
        )

        missing_technologies = [
            Technology(name=name) for name in set(names) - existing_names
        ]

        Technology.objects.bulk_create(missing_technologies, ignore_conflicts=True)

        technologies_objs = Technology.objects.filter(name__in=names)

        for technology_obj in technologies_objs:
            lesson.technologies.add(technology_obj)

        return lesson

    def create(self, validated_data):
        technologies = validated_data.pop("technologies", [])

        lesson = Lesson.objects.create(**validated_data)
        lesson = self.add_technology(lesson=lesson, technologies=technologies)
        lesson.save()

        if lesson.active:
            notify_lecturer(lesson=lesson)

        return lesson

    def update(self, instance: Lesson, validated_data):
        technologies = validated_data.pop("technologies", [])

        current_price = instance.price
        new_price = validated_data.get("price", instance.price)

        if current_price != new_price:
            LessonPriceHistory.objects.create(lesson=instance, price=current_price)

        Lesson.objects.filter(pk=instance.pk).update(**validated_data)

        instance.refresh_from_db()
        instance.technologies.clear()
        instance = self.add_technology(lesson=instance, technologies=technologies)
        instance.save()

        if instance.active:
            notify_lecturer(lesson=instance)

        return instance


class LessonPriceHistorySerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = LessonPriceHistory
        exclude = ("modified_at",)

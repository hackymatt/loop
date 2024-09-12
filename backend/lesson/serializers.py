from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    EmailField,
    CharField,
    ValidationError,
)
from drf_extra_fields.fields import Base64ImageField
from lesson.models import (
    Lesson,
    LessonPriceHistory,
)
from technology.models import Technology
from profile.models import LecturerProfile, Profile
from review.models import Review
from purchase.models import Purchase
from teaching.models import Teaching
from django.db.models.functions import Concat
from django.db.models import Avg, Value, Q
from django.conf import settings
from const import MIN_LESSON_DURATION_MINS
from notification.utils import notify
import urllib.parse


def notify_lecturer(lesson):
    for profile in Profile.objects.filter(user_type="W").all():
        notify(
            profile=profile,
            title="Nowa lekcja w ofercie",
            subtitle=lesson.title,
            description="Właśnie dodaliśmy nową lekcję. Zacznij ją prowadzić.",
            path=f"/account/teacher/teaching/?sort_by=title&page_size=10&title={urllib.parse.quote_plus(lesson.title)}",
            icon="mdi:teach",
        )


def get_lecturers(self, lessons):
    lecturer_ids = Teaching.objects.filter(lesson__in=lessons).values("lecturer")
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


def get_rating(lessons):
    return Review.objects.filter(lesson__in=lessons).aggregate(Avg("rating"))[
        "rating__avg"
    ]


def get_rating_count(lessons):
    return Review.objects.filter(lesson__in=lessons).count()


def get_students_count(lessons):
    return Purchase.objects.filter(lesson__in=lessons).count()


def get_lesson_technologies(lesson):
    lesson_technologies = (
        Lesson.technologies.through.objects.filter(lesson=lesson).all().order_by("id")
    )

    return [
        Technology.objects.get(id=lesson_technology.technology_id)
        for lesson_technology in lesson_technologies
    ]


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="profile.user.email")
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image", required=True)

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "email",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = (
            "modified_at",
            "created_at",
        )


class LessonGetSerializer(ModelSerializer):
    lecturers = SerializerMethodField("get_lesson_lecturers")
    students_count = SerializerMethodField("get_lesson_students_count")
    rating = SerializerMethodField("get_lesson_rating")
    rating_count = SerializerMethodField("get_lesson_rating_count")
    technologies = SerializerMethodField("get_technologies")

    def get_lesson_lecturers(self, lesson):
        return get_lecturers(self, lessons=[lesson])

    def get_lesson_rating(self, lesson):
        return get_rating(lessons=[lesson])

    def get_lesson_rating_count(self, lesson):
        return get_rating_count(lessons=[lesson])

    def get_lesson_students_count(self, lesson):
        return get_students_count(lessons=[lesson])

    def get_technologies(self, lesson):
        return TechnologySerializer(
            get_lesson_technologies(lesson=lesson), many=True
        ).data

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
        if duration % MIN_LESSON_DURATION_MINS != 0:
            raise ValidationError(
                f"Czas lekcji musi być wielokrotnością {MIN_LESSON_DURATION_MINS} minut."
            )

        return duration

    def validate_github_url(self, github_url):
        github_repo = settings.GITHUB_REPO
        if not github_url.startswith(github_repo):
            raise ValidationError(
                f"Github url musi być rozpoczynać się na {github_repo} minut."
            )

        return github_url

    def add_technology(self, lesson, technologies):
        for technology in technologies:
            lesson.technologies.add(technology)

        return lesson

    def create(self, validated_data):
        technologies = validated_data.pop("technologies")

        lesson = Lesson.objects.create(**validated_data)
        lesson = self.add_technology(lesson=lesson, technologies=technologies)
        lesson.save()

        if lesson.active:
            notify_lecturer(lesson=lesson)

        return lesson

    def update(self, instance, validated_data):
        technologies = validated_data.pop("technologies")

        current_price = instance.price
        new_price = validated_data.get("price", instance.price)

        if current_price != new_price:
            LessonPriceHistory.objects.create(lesson=instance, price=current_price)

        Lesson.objects.filter(pk=instance.pk).update(**validated_data)

        instance = Lesson.objects.get(pk=instance.pk)
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

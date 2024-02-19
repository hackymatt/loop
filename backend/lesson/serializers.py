from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    EmailField,
    IntegerField,
    ValidationError,
)
from drf_extra_fields.fields import Base64ImageField
from lesson.models import (
    Lesson,
    LessonPriceHistory,
    Technology,
)
from profile.models import Profile
from review.models import Review
from purchase.models import Purchase
from teaching.models import Teaching
from course.models import Course
from django.db.models.functions import Concat
from django.db.models import Avg, Value


MIN_LESSON_DURATION_MINS = 15


def get_lecturers(self, lessons):
    lecturer_ids = Teaching.objects.filter(lesson__in=lessons).values("lecturer")
    lecturers = (
        Profile.objects.filter(id__in=lecturer_ids)
        .annotate(full_name=Concat("user__first_name", Value(" "), "user__last_name"))
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


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="user.email")
    gender = EmailField(source="get_gender_display")
    image = Base64ImageField(required=True)

    class Meta:
        model = Profile
        fields = (
            "uuid",
            "email",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, profile):
        return profile.user.first_name + " " + profile.user.last_name


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = (
            "modified_at",
            "created_at",
        )


class LessonSerializer(ModelSerializer):
    lecturers = SerializerMethodField("get_lesson_lecturers")
    students_count = SerializerMethodField("get_lesson_students_count")
    rating = SerializerMethodField("get_lesson_rating")
    rating_count = SerializerMethodField("get_lesson_rating_count")
    technologies = TechnologySerializer(many=True)

    def get_lesson_lecturers(self, lesson):
        return get_lecturers(self, lessons=[lesson])

    def get_lesson_rating(self, lesson):
        return get_rating(lessons=[lesson])

    def get_lesson_rating_count(self, lesson):
        return get_rating_count(lessons=[lesson])

    def get_lesson_students_count(self, lesson):
        return get_students_count(lessons=[lesson])

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

    def add_technology(self, lesson, technologies):
        objs = []
        for technology in technologies:
            obj, _ = Technology.objects.get_or_create(name=technology["name"])
            objs.append(obj)

        lesson.technologies.add(*objs)

        return lesson

    def create(self, validated_data):
        technologies = validated_data.pop("technologies")

        lesson = Lesson.objects.create(**validated_data)
        lesson = self.add_technology(lesson=lesson, technologies=technologies)
        lesson.save()

        return lesson

    def update(self, instance, validated_data):
        technologies = validated_data.pop("technologies")

        current_price = instance.price
        new_price = validated_data.get("price", instance.price)

        if current_price != new_price:
            LessonPriceHistory.objects.create(lesson=instance, price=current_price)

        Lesson.objects.filter(pk=instance.pk).update(**validated_data)

        instance = Lesson.objects.get(pk=instance.pk)
        instance = self.add_technology(lesson=instance, technologies=technologies)
        instance.save()

        return instance


class LessonPriceHistorySerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = LessonPriceHistory
        exclude = ("modified_at",)


class TechnologyListSerializer(ModelSerializer):
    courses_count = SerializerMethodField("get_course_count")

    class Meta:
        model = Technology
        exclude = (
            "modified_at",
            "created_at",
        )

    def get_course_count(self, technology):
        lessons = Lesson.technologies.through.objects.filter(
            technology_id=technology
        ).values("lesson_id")
        courses = (
            Course.lessons.through.objects.filter(lesson_id__in=lessons)
            .values("course_id")
            .distinct()
        )
        return courses.count()

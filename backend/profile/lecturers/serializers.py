from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    SerializerMethodField,
)
from drf_extra_fields.fields import Base64ImageField
from profile.models import LecturerProfile
from lesson.models import Lesson
from math import ceil


def format_rating(value):
    if value is None:
        return None
    return ceil(value * 10) / 10


def get_lessons(lecturer: LecturerProfile):
    ids = lecturer.lessons
    return (
        Lesson.objects.filter(id__in=ids)
        .add_previous_price()
        .add_lowest_30_days_price()
    )


def get_previous_price(lecturer: LecturerProfile):
    lessons = get_lessons(lecturer=lecturer)
    prices = []
    for lesson in lessons:
        prev = lesson.previous_price
        curr = lesson.price
        if prev is None:
            prev = curr

        prices.append(prev)

    previous_price = sum(prices)
    current_price = lecturer.lessons_price

    if previous_price <= current_price:
        return None

    return previous_price


def get_lowest_30_days_price(lecturer: LecturerProfile):
    lessons = get_lessons(lecturer=lecturer)
    prices = []
    for lesson in lessons:
        prev = lesson.previous_price
        curr = lesson.price
        if prev is None:
            prev = curr

        prices.append(prev)

    lowest_30_days_price = sum(prices)

    if not get_previous_price(lecturer=lecturer):
        return None

    return lowest_30_days_price


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.get_gender_display")
    rating = SerializerMethodField()
    rating_count = SerializerMethodField()
    lessons_count = SerializerMethodField()
    lessons_duration = SerializerMethodField()
    students_count = SerializerMethodField()
    image = Base64ImageField(source="profile.image")

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "title",
            "description",
            "image",
            "rating",
            "rating_count",
            "lessons_count",
            "lessons_duration",
            "students_count",
            "linkedin_url",
        )

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name

    def get_rating(self, lecturer: LecturerProfile):
        return format_rating(lecturer.rating)

    def get_rating_count(self, lecturer: LecturerProfile):
        return lecturer.rating_count

    def get_lessons_count(self, lecturer: LecturerProfile):
        return lecturer.lessons_count

    def get_lessons_duration(self, lecturer: LecturerProfile):
        return lecturer.lessons_duration

    def get_students_count(self, lecturer: LecturerProfile):
        return lecturer.students_count


class LessonShortSerializer(ModelSerializer):
    previous_price = SerializerMethodField()
    lowest_30_days_price = SerializerMethodField()

    def get_previous_price(self, lesson: Lesson):
        return lesson.previous_price

    def get_lowest_30_days_price(self, lesson: Lesson):
        return lesson.lowest_30_days_price

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "price",
            "previous_price",
            "lowest_30_days_price",
        )


class LecturerGetSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.get_gender_display")
    rating = SerializerMethodField()
    rating_count = SerializerMethodField()
    lessons = SerializerMethodField()
    lessons_duration = SerializerMethodField()
    image = Base64ImageField(source="profile.image")
    lessons_price = SerializerMethodField()
    lessons_previous_price = SerializerMethodField()
    lessons_lowest_30_days_price = SerializerMethodField()
    students_count = SerializerMethodField()

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "title",
            "description",
            "linkedin_url",
            "image",
            "rating",
            "rating_count",
            "lessons",
            "lessons_duration",
            "lessons_price",
            "lessons_previous_price",
            "lessons_lowest_30_days_price",
            "students_count",
        )

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name

    def get_rating(self, lecturer: LecturerProfile):
        return format_rating(lecturer.rating)

    def get_rating_count(self, lecturer: LecturerProfile):
        return lecturer.rating_count

    def get_lessons(self, lecturer: LecturerProfile):
        return LessonShortSerializer(get_lessons(lecturer=lecturer), many=True).data

    def get_lessons_duration(self, lecturer: LecturerProfile):
        return lecturer.lessons_duration

    def get_lessons_price(self, lecturer: LecturerProfile):
        return lecturer.lessons_price

    def get_lessons_previous_price(self, lecturer: LecturerProfile):
        return get_previous_price(lecturer=lecturer)

    def get_lessons_lowest_30_days_price(self, lecturer: LecturerProfile):
        return get_lowest_30_days_price(lecturer=lecturer)

    def get_students_count(self, lecturer: LecturerProfile):
        return lecturer.students_count


class BestLecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image")

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "title",
            "image",
            "linkedin_url",
        )

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    SerializerMethodField,
)
from drf_extra_fields.fields import Base64ImageField
from profile.models import LecturerProfile
from review.models import Review
from teaching.models import Teaching
from lesson.models import Lesson, LessonPriceHistory
from reservation.models import Reservation
from django.db.models import Sum, Avg, Min, Subquery, OuterRef
from datetime import timedelta


def get_rating(lecturer):
    return Review.objects.filter(lecturer=lecturer)


def get_lessons(lecturer):
    ids = Teaching.objects.filter(lecturer=lecturer).values("lesson")
    return Lesson.objects.filter(id__in=ids)


def get_duration(lecturer):
    lessons = get_lessons(lecturer=lecturer)
    duration = Lesson.objects.filter(pk=OuterRef("lesson__id")).values("duration")
    reservations = Reservation.objects.filter(lesson__in=lessons).annotate(
        duration=Subquery(duration)
    )
    return reservations.aggregate(Sum("duration"))["duration__sum"]


def get_previous_prices(instance):
    previous_prices = (
        LessonPriceHistory.objects.filter(lesson=instance).order_by("-created_at").all()
    )

    return previous_prices


def get_previous_price(instance):
    current_price = instance.price
    previous_prices = get_previous_prices(instance)

    if previous_prices.count() == 0:
        return None

    last_price_change = previous_prices.first()

    previous_price = last_price_change.price

    if previous_price <= current_price:
        return None

    return previous_price


def get_price(instance):
    lessons = get_lessons(lecturer=instance)
    return lessons.aggregate(Sum("price"))["price__sum"]


def get_previous_price_course(instance):
    lessons = get_lessons(lecturer=instance)
    prices = []
    for lesson in lessons:
        prev = get_previous_price(lesson)
        curr = lesson.price
        if prev is None:
            prev = curr

        prices.append(prev)

    previous_price = sum(prices)
    current_price = get_price(instance=instance)

    if previous_price <= current_price:
        return None

    return previous_price


def get_lowest_30_days_price(instance):
    current_price = instance.price
    previous_prices = get_previous_prices(instance)

    if previous_prices.count() == 0:
        return None

    last_price_change = previous_prices.first()

    previous_price = last_price_change.price

    if previous_price <= current_price:
        return None

    last_price_change_date = last_price_change.created_at
    last_price_change_date_minus_30_days = last_price_change.created_at - timedelta(
        days=30
    )

    prices_in_last_30_days = previous_prices.filter(
        created_at__lte=last_price_change_date,
        created_at__gte=last_price_change_date_minus_30_days,
    )

    return prices_in_last_30_days.aggregate(Min("price"))["price__min"]


def get_lowest_30_days_price_course(instance):
    lessons = get_lessons(lecturer=instance)
    prices = []
    for lesson in lessons:
        prev = get_lowest_30_days_price(lesson)
        curr = lesson.price
        if prev is None:
            prev = curr

        prices.append(prev)

    lowest_30_days_price = sum(prices)

    if not get_previous_price_course(instance=instance):
        return None

    return lowest_30_days_price


def get_students_count(lecturer):
    return Reservation.objects.filter(schedule__lecturer=lecturer).count()


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    gender = CharField(source="profile.get_gender_display")
    rating = SerializerMethodField("get_lecturer_rating")
    rating_count = SerializerMethodField("get_lecturer_rating_count")
    lessons_count = SerializerMethodField("get_lecturer_lessons_count")
    lessons_duration = SerializerMethodField("get_lecturer_lessons_duration")
    students_count = SerializerMethodField("get_lecturer_students_count")
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
        )

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name

    def get_lecturer_rating(self, lecturer):
        return get_rating(lecturer=lecturer).aggregate(Avg("rating"))["rating__avg"]

    def get_lecturer_rating_count(self, lecturer):
        return get_rating(lecturer=lecturer).count()

    def get_lecturer_lessons_count(self, lecturer):
        return get_lessons(lecturer=lecturer).count()

    def get_lecturer_lessons_duration(self, lecturer):
        return get_duration(lecturer=lecturer)

    def get_lecturer_students_count(self, lecturer):
        return get_students_count(lecturer=lecturer)


class LessonShortSerializer(ModelSerializer):
    previous_price = SerializerMethodField("get_lesson_previous_price")
    lowest_30_days_price = SerializerMethodField("get_lesson_lowest_30_days_price")

    def get_lesson_previous_price(self, lesson):
        return get_previous_price(instance=lesson)

    def get_lesson_lowest_30_days_price(self, lesson):
        return get_lowest_30_days_price(instance=lesson)

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
    full_name = SerializerMethodField("get_full_name")
    gender = CharField(source="profile.get_gender_display")
    email = EmailField(source="profile.user.email")
    rating = SerializerMethodField("get_lecturer_rating")
    rating_count = SerializerMethodField("get_lecturer_rating_count")
    lessons = SerializerMethodField("get_lecturer_lessons")
    lessons_duration = SerializerMethodField("get_lecturer_lessons_duration")
    image = Base64ImageField(source="profile.image")
    lessons_price = SerializerMethodField("get_lecturer_lessons_price")
    lessons_previous_price = SerializerMethodField(
        "get_lecturer_lessons_previous_price"
    )
    lessons_lowest_30_days_price = SerializerMethodField(
        "get_lecturer_lessons_lowest_30_days_price"
    )
    students_count = SerializerMethodField("get_lecturer_students_count")

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "email",
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

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name

    def get_lecturer_rating(self, lecturer):
        return get_rating(lecturer=lecturer).aggregate(Avg("rating"))["rating__avg"]

    def get_lecturer_rating_count(self, lecturer):
        return get_rating(lecturer=lecturer).count()

    def get_lecturer_lessons(self, lecturer):
        return LessonShortSerializer(get_lessons(lecturer=lecturer), many=True).data

    def get_lecturer_lessons_duration(self, lecturer):
        return get_duration(lecturer=lecturer)

    def get_lecturer_lessons_price(self, lecturer):
        return get_price(instance=lecturer)

    def get_lecturer_lessons_previous_price(self, lecturer):
        return get_previous_price_course(instance=lecturer)

    def get_lecturer_lessons_lowest_30_days_price(self, lecturer):
        return get_lowest_30_days_price_course(instance=lecturer)

    def get_lecturer_students_count(self, lecturer):
        return get_students_count(lecturer=lecturer)


class BestLecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
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
        )

    def get_full_name(self, lecturer):
        return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name

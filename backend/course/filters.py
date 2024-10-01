from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    BaseInFilter,
    NumberFilter,
)
from course.models import (
    Course,
)
from lesson.models import Lesson, Technology
from module.models import Module
from review.models import Review
from purchase.models import Purchase
from teaching.models import Teaching
from profile.models import LecturerProfile
from reservation.models import Reservation
from django.db.models import (
    OuterRef,
    Subquery,
    Value,
    Avg,
    Sum,
    Count,
    TextField,
    Case,
    When,
    FloatField,
    F,
)
from django.contrib.postgres.aggregates import StringAgg
from django.db.models.functions import Cast, Coalesce
from datetime import datetime
from django.utils.timezone import make_aware


def get_rating(queryset):
    course_modules = (
        Course.modules.through.objects.filter(course=OuterRef(OuterRef(OuterRef("pk"))))
        .values("module_id")
        .order_by("id")
    )
    lessons = (
        Module.lessons.through.objects.filter(module__in=Subquery(course_modules))
        .values("lesson_id")
        .order_by("id")
    )
    avg_rating = (
        Review.objects.filter(lesson__in=Subquery(lessons))
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(avg_rating=Avg("rating"))
        .values("avg_rating")
    )
    courses = queryset.annotate(rating=Subquery(avg_rating))

    return courses


def get_duration(queryset):
    course_modules = (
        Course.modules.through.objects.filter(course=OuterRef(OuterRef(OuterRef("pk"))))
        .values("module_id")
        .order_by("id")
    )
    lessons = (
        Module.lessons.through.objects.filter(module__in=Subquery(course_modules))
        .values("lesson_id")
        .order_by("id")
    )

    total_duration = (
        Lesson.objects.filter(id__in=Subquery(lessons))
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(total_duration=Sum("duration"))
        .values("total_duration")
    )
    courses = queryset.annotate(duration=Subquery(total_duration))

    return courses


def get_price(queryset):
    course_modules = (
        Course.modules.through.objects.filter(course=OuterRef(OuterRef(OuterRef("pk"))))
        .values("module_id")
        .order_by("id")
    )
    lessons = (
        Module.lessons.through.objects.filter(module__in=Subquery(course_modules))
        .values("lesson_id")
        .order_by("id")
    )

    total_price = (
        Lesson.objects.filter(id__in=Subquery(lessons))
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(total_price=Sum("price"))
        .values("total_price")
    )
    courses = queryset.annotate(price=Subquery(total_price))

    return courses


def get_students_count(queryset):
    course_modules = (
        Course.modules.through.objects.filter(course=OuterRef(OuterRef(OuterRef("pk"))))
        .values("module_id")
        .order_by("id")
    )
    lessons = (
        Module.lessons.through.objects.filter(module__in=Subquery(course_modules))
        .values("lesson_id")
        .order_by("id")
    )

    total_student_count = (
        Purchase.objects.filter(lesson__in=Subquery(lessons))
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(total_student_count=Count("student"))
        .values("total_student_count")
    )
    courses = queryset.annotate(
        students_count=Coalesce(Subquery(total_student_count), Value(0))
    )

    return courses


def get_progress(queryset):
    course_modules = (
        Course.modules.through.objects.filter(course=OuterRef(OuterRef(OuterRef("pk"))))
        .values("module_id")
        .order_by("id")
    )
    lessons = (
        Module.lessons.through.objects.filter(module__in=Subquery(course_modules))
        .values("lesson_id")
        .order_by("id")
    )

    total_completed_count = (
        Reservation.objects.filter(
            student__profile__user__email=OuterRef("user_email"),
            lesson__in=Subquery(lessons),
            schedule__end_time__lte=make_aware(datetime.now()),
        )
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(total_completed_count=Count("lesson"))
        .values("total_completed_count")
    )

    total_lessons_count = (
        Lesson.objects.filter(id__in=Subquery(lessons))
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(total_lessons_count=Count("pk"))
        .values("total_lessons_count")
    )

    courses = queryset.annotate(
        completed_lessons_count=Subquery(total_completed_count),
        all_lessons_count=Subquery(total_lessons_count),
    ).annotate(
        progress=Case(
            When(all_lessons_count__isnull=True, then=Value(0.0)),
            When(all_lessons_count=0, then=Value(0.0)),
            When(completed_lessons_count__isnull=True, then=Value(0.0)),
            default=F("completed_lessons_count") * 1.0 / F("all_lessons_count"),
            output_field=FloatField(),
        )
    )

    return courses


def get_lecturers(queryset):
    course_modules = (
        Course.modules.through.objects.filter(
            course=OuterRef(OuterRef(OuterRef(OuterRef("pk"))))
        )
        .values("module_id")
        .order_by("id")
    )
    lessons = (
        Module.lessons.through.objects.filter(module__in=Subquery(course_modules))
        .values("lesson_id")
        .order_by("id")
    )

    lecturers = (
        Teaching.objects.filter(lesson__in=Subquery(lessons))
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .values("lecturer")
        .distinct()
    )

    profiles = (
        LecturerProfile.objects.filter(id__in=Subquery(lecturers))
        .values("id")
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(ids=StringAgg(Cast("id", TextField()), delimiter=","))
        .values("ids")
    )

    courses = queryset.annotate(all_lecturers=Subquery(profiles))

    return courses


def get_technologies(queryset):
    course_modules = (
        Course.modules.through.objects.filter(
            course=OuterRef(OuterRef(OuterRef(OuterRef("pk"))))
        )
        .values("module_id")
        .order_by("id")
    )
    lessons = (
        Module.lessons.through.objects.filter(module__in=Subquery(course_modules))
        .values("lesson_id")
        .order_by("id")
    )

    technologies = (
        Lesson.technologies.through.objects.filter(lesson_id__in=Subquery(lessons))
        .values("technology_id")
        .distinct()
    )

    all_technologies = (
        Technology.objects.filter(id__in=Subquery(technologies))
        .values("name")
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(names=StringAgg("name", delimiter=","))
        .values("names")
    )

    courses = queryset.annotate(all_technologies=Subquery(all_technologies))

    return courses


class CharInFilter(BaseInFilter, CharFilter):
    pass


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if value in ["duration", "-duration"]:
                queryset = get_duration(queryset).order_by(value)
            elif value in ["price", "-price"]:
                queryset = get_price(queryset).order_by(value)
            elif value in ["rating", "-rating"]:
                queryset = get_rating(queryset).order_by(value)
            elif value in ["students_count", "-students_count"]:
                queryset = get_students_count(queryset).order_by(value)
            elif value in ["progress", "-progress"]:
                queryset = get_progress(queryset).order_by(value)
            else:
                queryset = queryset.order_by(value)

        return queryset


class CourseFilter(FilterSet):
    lecturer_in = CharFilter(
        label="Lecturer in",
        field_name="all_lecturers",
        method="filter_lecturer_in",
    )
    technology_in = CharFilter(
        label="Technology in",
        field_name="all_technologies",
        method="filter_technology_in",
    )
    level_in = CharInFilter(field_name="level", lookup_expr="in")
    price_from = NumberFilter(
        label="Price powyżej lub równe",
        field_name="price",
        method="filter_price_from",
    )
    price_to = NumberFilter(
        label="Price poniżej lub równe",
        field_name="price",
        method="filter_price_to",
    )
    rating_from = NumberFilter(
        label="Rating powyżej lub równe",
        field_name="rating",
        method="filter_rating_from",
    )
    duration_from = NumberFilter(
        label="Duration powyżej lub równe",
        field_name="duration",
        method="filter_duration_from",
    )
    duration_to = NumberFilter(
        label="Duration poniżej lub równe",
        field_name="duration",
        method="filter_duration_to",
    )
    sort_by = OrderFilter(
        choices=(
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
            ("level", "Level ASC"),
            ("-level", "Level DESC"),
            ("price", "Price ASC"),
            ("-price", "Price DESC"),
            ("duration", "Duration ASC"),
            ("-duration", "Duration DESC"),
            ("rating", "Rating ASC"),
            ("-rating", "Rating DESC"),
            ("students_count", "Students Count ASC"),
            ("-students_count", "Students Count DESC"),
            ("progress", "Progress ASC"),
            ("-progress", "Progress DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
            "level": "level",
            "level": "-level",
            "price": "price",
            "price": "-price",
            "duration": "duration",
            "duration": "-duration",
            "rating": "rating",
            "rating": "-rating",
            "students_count": "students_count",
            "students_count": "-students_count",
            "progress": "progress",
            "progress": "-progress",
        },
    )

    class Meta:
        model = Course
        fields = (
            "lecturer_in",
            "technology_in",
            "level_in",
            "price_from",
            "price_to",
            "rating_from",
            "duration_from",
            "duration_to",
            "active",
            "sort_by",
        )

    def filter_technology_in(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__contains"

        queryset = get_technologies(queryset)

        names = value.split(",")

        name_first, *name_rest = names
        return_queryset = queryset.filter(**{lookup_field_name: name_first})
        for name in name_rest:
            return_queryset = return_queryset | queryset.filter(
                **{lookup_field_name: name}
            )

        return return_queryset

    def filter_lecturer_in(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__contains"

        queryset = get_lecturers(queryset)

        ids = value.split(",")

        id_first, *id_rest = ids
        return_queryset = queryset.filter(**{lookup_field_name: id_first})
        for id in id_rest:
            return_queryset = return_queryset | queryset.filter(
                **{lookup_field_name: id}
            )

        return return_queryset

    def filter_rating_from(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__gte"
        return get_rating(queryset).filter(**{lookup_field_name: value})

    def filter_duration_from(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__gte"
        return get_duration(queryset).filter(**{lookup_field_name: value})

    def filter_price_from(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__gte"
        return get_price(queryset).filter(**{lookup_field_name: value})

    def filter_price_to(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__lte"
        return get_price(queryset).filter(**{lookup_field_name: value})

    def filter_duration_to(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__lte"
        return get_duration(queryset).filter(**{lookup_field_name: value})

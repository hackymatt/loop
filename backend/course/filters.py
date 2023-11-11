from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    BaseInFilter,
    NumberFilter,
)
from course.models import Course, Lesson
from review.models import Review
from django.db.models import OuterRef, Subquery, Value, Avg, Sum


def get_rating(queryset):
    lessons = Lesson.objects.filter(course=OuterRef(OuterRef("pk"))).values("id")
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
    total_duration = (
        Lesson.objects.filter(course=OuterRef("pk"))
        .values("course__pk")
        .annotate(total_duration=Sum("duration"))
        .values("total_duration")
    )
    courses = queryset.annotate(duration=Subquery(total_duration))

    return courses


class CharInFilter(BaseInFilter, CharFilter):
    pass


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if value in ["technology", "-technology"]:
                queryset = queryset.order_by(f"{value}__name")
            elif value in ["duration", "-duration"]:
                queryset = get_duration(queryset).order_by(value)
            elif value in ["rating", "-rating"]:
                queryset = get_rating(queryset).order_by(value)
            else:
                queryset = queryset.order_by(value)

        return queryset


class CourseFilter(FilterSet):
    technology_in = CharInFilter(field_name="technology__name", lookup_expr="in")
    level_in = CharInFilter(field_name="level", lookup_expr="in")
    price_from = NumberFilter(field_name="price", lookup_expr="gte")
    price_to = NumberFilter(field_name="price", lookup_expr="lte")
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
            ("technology", "Technology ASC"),
            ("-technology", "Technology DESC"),
            ("level", "Level ASC"),
            ("-level", "Level DESC"),
            ("price", "Price ASC"),
            ("-price", "price DESC"),
            ("duration", "Duration ASC"),
            ("-duration", "Duration DESC"),
            ("rating", "Rating ASC"),
            ("-rating", "Rating DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
            "technology__name": "technology",
            "technology__name": "-technology",
            "level": "level",
            "level": "-level",
            "price": "price",
            "price": "-price",
            "duration": "duration",
            "duration": "-duration",
            "rating": "rating",
            "rating": "-rating",
        },
    )

    class Meta:
        model = Course
        fields = (
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

    def filter_rating_from(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__gte"
        return get_rating(queryset).filter(**{lookup_field_name: value})

    def filter_duration_from(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__gte"
        return get_duration(queryset).filter(**{lookup_field_name: value})

    def filter_duration_to(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__lte"
        return get_duration(queryset).filter(**{lookup_field_name: value})

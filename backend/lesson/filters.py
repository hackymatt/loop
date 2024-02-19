from django_filters import (
    FilterSet,
    OrderingFilter,
    NumberFilter,
    CharFilter,
    DateFilter,
)
from lesson.models import (
    LessonPriceHistory,
    Lesson,
)
from course.models import Course
from django.db.models import OuterRef, Subquery, Value, Avg, Sum, Count, TextField


def get_courses_count(queryset):
    lessons = Lesson.technologies.through.objects.filter(
        technology_id=OuterRef(OuterRef("pk"))
    ).values("lesson_id")
    total_courses_count = (
        Course.lessons.through.objects.filter(lesson_id__in=Subquery(lessons))
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(total_courses_count=Count("id"))
        .values("total_courses_count")
    )
    technologies = queryset.annotate(courses_count=Subquery(total_courses_count))

    return technologies


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if value in ["lesson_name", "-lesson_name"]:
                value_modified = value.replace("_name", "__title")
                queryset = get_courses_count(queryset).order_by(value_modified)
            else:
                queryset = queryset.order_by(value)

        return queryset


class LessonPriceHistoryFilter(FilterSet):
    lesson_name = CharFilter(field_name="lesson__title", lookup_expr="icontains")
    price_from = NumberFilter(field_name="price", lookup_expr="gte")
    price_to = NumberFilter(field_name="price", lookup_expr="lte")
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")
    sort_by = OrderFilter(
        choices=(
            ("lesson_name", "Lesson Name ASC"),
            ("-lesson_name", "Lesson Name  DESC"),
            ("price", "Price ASC"),
            ("-price", "Price  DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "lesson_name": "lesson_name",
            "-lesson_name": "-lesson_name",
            "price": "price",
            "-price": "-price",
            "created_at": "created_at",
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = LessonPriceHistory
        fields = (
            "lesson_name",
            "price_from",
            "price_to",
            "created_at",
            "sort_by",
        )


class LessonFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    duration_from = NumberFilter(field_name="duration", lookup_expr="gte")
    duration_to = NumberFilter(field_name="duration", lookup_expr="lte")
    price_from = NumberFilter(field_name="price", lookup_expr="gte")
    price_to = NumberFilter(field_name="price", lookup_expr="lte")
    github_url = CharFilter(field_name="github_url", lookup_expr="icontains")
    active = CharFilter(field_name="active", lookup_expr="exact")
    sort_by = OrderFilter(
        choices=(
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
            ("duration", "Duration ASC"),
            ("-duration", "Duration DESC"),
            ("price", "Price ASC"),
            ("-price", "Price DESC"),
            ("github_url", "Github Url ASC"),
            ("-github_url", "Github Url DESC"),
            ("active", "Active ASC"),
            ("-active", "Active DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
            "duration": "duration",
            "-duration": "-duration",
            "price": "price",
            "-price": "-price",
            "github_url": "github_url",
            "-github_url": "-github_url",
            "active": "active",
            "-active": "-active",
        },
    )

    class Meta:
        model = Lesson
        fields = (
            "title",
            "duration_from",
            "duration_to",
            "price_from",
            "price_to",
            "github_url",
            "active",
            "sort_by",
        )

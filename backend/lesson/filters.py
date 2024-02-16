from django_filters import (
    FilterSet,
    OrderingFilter,
    NumberFilter,
    CharFilter,
)
from lesson.models import (
    LessonPriceHistory,
    Technology,
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
            if value in ["courses_count", "-courses_count"]:
                queryset = get_courses_count(queryset).order_by(value)
            else:
                queryset = queryset.order_by(value)

        return queryset


class LessonPriceHistoryFilter(FilterSet):
    lesson_id = NumberFilter(field_name="lesson__id", lookup_expr="exact")
    sort_by = OrderFilter(
        choices=(
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "created_at": "created_at",
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = LessonPriceHistory
        fields = (
            "lesson_id",
            "sort_by",
        )


class TechnologyFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="exact")
    sort_by = OrderFilter(
        choices=(
            ("name", "Name ASC"),
            ("-name", "Name DESC"),
            ("courses_count", "Courses Count ASC"),
            ("-courses_count", "Courses Count DESC"),
        ),
        fields={
            "name": "name",
            "-name": "-name",
            "courses_count": "courses_count",
            "-courses_count": "-courses_count",
        },
    )

    class Meta:
        model = Technology
        fields = (
            "name",
            "sort_by",
        )

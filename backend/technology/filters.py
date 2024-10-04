from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    DateFilter,
    NumberFilter,
)
from lesson.models import (
    Lesson,
)
from technology.models import Technology
from course.models import Course
from module.models import Module
from django.db.models import OuterRef, Subquery, Value, Count, FloatField
from django.db.models.functions import Coalesce


def get_courses_count(queryset):
    lessons = Lesson.technologies.through.objects.filter(
        technology_id=OuterRef(OuterRef(OuterRef("pk")))
    ).values("lesson_id")
    modules = Module.lessons.through.objects.filter(
        lesson_id__in=Subquery(lessons)
    ).values("module_id")
    total_courses_count = (
        Course.modules.through.objects.filter(module_id__in=Subquery(modules))
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(total_courses_count=Count("id"))
        .values("total_courses_count")
    )
    technologies = queryset.annotate(
        courses_count=Coalesce(
            Subquery(total_courses_count), Value(0), output_field=FloatField()
        )
    )

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


class TechnologyFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    courses_count_from = NumberFilter(
        label="Liczba kursów większa lub równa",
        field_name="courses_count",
        method="filter_courses_count_from",
    )
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")
    sort_by = OrderFilter(
        choices=(
            ("name", "Name ASC"),
            ("-name", "Name DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
            ("courses_count", "Courses Count ASC"),
            ("-courses_count", "Courses Count DESC"),
        ),
        fields={
            "name": "name",
            "-name": "-name",
            "created_at": "created_at",
            "-created_at": "-created_at",
            "courses_count": "courses_count",
            "-courses_count": "-courses_count",
        },
    )

    class Meta:
        model = Technology
        fields = (
            "name",
            "created_at",
            "sort_by",
        )

    def filter_courses_count_from(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__gte"
        return get_courses_count(queryset).filter(**{lookup_field_name: value})

from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    DateFilter,
    NumberFilter,
)
from technology.models import Technology


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
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
        return queryset.filter(**{lookup_field_name: value})

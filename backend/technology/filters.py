from django_filters import (
    FilterSet,
    CharFilter,
    DateFilter,
    NumberFilter,
)
from technology.models import Technology
from utils.ordering.ordering import OrderFilter


class TechnologyFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    courses_count_from = NumberFilter(field_name="courses_count", lookup_expr="gte")
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

from django_filters import (
    FilterSet,
    CharFilter,
    DateFilter,
)
from tag.models import Tag
from utils.ordering.ordering import OrderFilter


class TagFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")
    sort_by = OrderFilter(
        choices=(
            ("name", "Name ASC"),
            ("-name", "Name DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "name": "name",
            "-name": "-name",
            "created_at": "created_at",
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = Tag
        fields = (
            "name",
            "created_at",
            "sort_by",
        )

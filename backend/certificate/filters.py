from django_filters import (
    FilterSet,
    CharFilter,
    DateFilter,
)
from certificate.models import Certificate
from utils.ordering.ordering import OrderFilter


class CertificateFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    type = CharFilter(field_name="type", lookup_expr="exact")
    completed_at = DateFilter(field_name="completed_at", lookup_expr="contains")

    sort_by = OrderFilter(
        choices=(
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
            ("type", "Type ASC"),
            ("-type", "Type DESC"),
            ("completed_at", "Completed At ASC"),
            ("-completed_at", "Completed At DESC"),
        ),
        fields={
            "name": "name",
            "-name": "-name",
            "type": "type",
            "-type": "type",
            "completed_at": "completed_at",
            "-completed_at": "-completed_at",
        },
    )

    class Meta:
        model = Certificate
        fields = (
            "title",
            "type",
            "completed_at",
            "sort_by",
        )

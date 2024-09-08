from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    DateFilter,
)
from certificate.models import Certificate
from django.db.models import F
from django.utils import timezone
from django.db.models import ExpressionWrapper, DurationField


def get_completed_at(queryset):
    return queryset.annotate(
        completed_at=ExpressionWrapper(
            F("created_at") - timezone.timedelta(days=1),
            output_field=DurationField(),
        )
    )


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if value in ["completed_at", "-completed_at"]:
                value_modified = value.replace("completed_at", "created_at")
                queryset = queryset.order_by(value_modified)
            else:
                queryset = queryset.order_by(value)

        return queryset


class CertificateFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    type = CharFilter(field_name="type", lookup_expr="exact")
    completed_at = DateFilter(
        label="Completed at równe",
        field_name="completed_at",
        method="filter_completed_at",
    )

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

    def filter_completed_at(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__icontains"
        return get_completed_at(queryset).filter(**{lookup_field_name: value})

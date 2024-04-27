from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    UUIDFilter,
    DateFilter,
    BooleanFilter,
)
from newsletter.models import Newsletter


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class NewsletterFilter(FilterSet):
    uuid = UUIDFilter(field_name="uuid", lookup_expr="exact")
    email = CharFilter(field_name="email", lookup_expr="icontains")
    active = BooleanFilter(field_name="active", lookup_expr="exact")
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")
    sort_by = OrderFilter(
        choices=(
            ("uuid", "Id ASC"),
            ("-uuid", "Id DESC"),
            ("email", "Email ASC"),
            ("-email", "Email DESC"),
            ("active", "Active ASC"),
            ("-active", "Active DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "uuid": "uuid",
            "-uuid": "-uuid",
            "email": "email",
            "-email": "-email",
            "active": "active",
            "-active": "-active",
            "created_at": "created_at",
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = Newsletter
        fields = (
            "uuid",
            "email",
            "active",
            "created_at",
            "sort_by",
        )

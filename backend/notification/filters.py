from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
)
from notification.models import Notification


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class NotificationFilter(FilterSet):
    status = CharFilter(field_name="status", lookup_expr="exact")
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
        model = Notification
        fields = (
            "status",
            "sort_by",
        )

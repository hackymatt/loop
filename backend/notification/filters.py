from django_filters import (
    FilterSet,
    CharFilter,
)
from notification.models import Notification
from utils.ordering.ordering import OrderFilter


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

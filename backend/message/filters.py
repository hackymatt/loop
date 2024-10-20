from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
)
from message.models import Message


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class MessageFilter(FilterSet):
    type = CharFilter(field_name="type", lookup_expr="exact")
    status = CharFilter(field_name="status", lookup_expr="exact")
    sort_by = OrderFilter(
        choices=(
            ("sender", "Sender ASC"),
            ("-sender", "Sender DESC"),
            ("recipient", "Recipient ASC"),
            ("-recipient", "Recipient DESC"),
            ("subject", "Subject ASC"),
            ("-subject", "Subject DESC"),
            ("status", "Status ASC"),
            ("-status", "Status DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "sender": "sender__full_name",
            "-sender": "-sender__full_namer",
            "recipient": "recipient__full_name",
            "-recipient": "-recipient__full_name",
            "subject": "subject",
            "-subject": "-subject",
            "status": "status",
            "-status": "-status",
            "created_at": "created_at",
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = Message
        fields = (
            "type",
            "status",
            "sort_by",
        )

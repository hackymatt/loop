from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
)
from message.models import Message
from django.db.models import Case, When, Value, CharField, F
from django.db.models.functions import Concat


def get_type(queryset):
    messages = queryset.annotate(
        type=Case(
            When(profile_id=F("recipient__id"), then=Value("INBOX")),
            default=Value("SENT"),
            output_field=CharField(),
        )
    )

    return messages


def get_sender_full_name(queryset):
    messages = queryset.annotate(
        sender_full_name=Concat(
            "sender__user__first_name", Value(" "), "sender__user__last_name"
        )
    )

    return messages


def get_recipient_full_name(queryset):
    messages = queryset.annotate(
        recipient_full_name=Concat(
            "recipient__user__first_name", Value(" "), "recipient__user__last_name"
        )
    )

    return messages


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if value in ["sender", "-sender"]:
                modified_value = f"{value}_full_name"
                queryset = get_sender_full_name(queryset).order_by(modified_value)
            elif value in ["recipient", "-recipient"]:
                modified_value = f"{value}_full_name"
                queryset = get_recipient_full_name(queryset).order_by(modified_value)
            else:
                queryset = queryset.order_by(value)

        return queryset


class MessageFilter(FilterSet):
    type = CharFilter(
        label="Rodzaj wiadomości",
        field_name="type",
        method="filter_type",
    )
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
            "sender": "sender",
            "-sender": "-sender",
            "recipient": "recipient",
            "-recipient": "-recipient",
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

    def filter_type(self, queryset, field_name, value):
        lookup_field_name = field_name
        return get_type(queryset).filter(**{lookup_field_name: value})

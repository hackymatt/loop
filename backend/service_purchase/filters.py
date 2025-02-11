from django_filters import (
    FilterSet,
    CharFilter,
    NumberFilter,
    DateFilter,
)
from service_purchase.models import Purchase, Payment
from utils.ordering.ordering import OrderFilter


class PurchaseOrderFilter(OrderFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if "service_title" in value:
                queryset = queryset.order_by(value.replace("_", "__"))
            else:
                queryset = queryset.order_by(value)

        return queryset


class PurchaseFilter(FilterSet):
    service_title = CharFilter(field_name="service__title", lookup_expr="icontains")
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")

    sort_by = PurchaseOrderFilter(
        choices=(
            ("service_title", "Service Title ASC"),
            ("-service_title", "Service Title DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "service_title": "service__title",
            "-service_title": "-service__title",
            "created_at": "created_at",
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = Purchase
        fields = (
            "service_title",
            "created_at",
            "sort_by",
        )


class PaymentFilter(FilterSet):
    session_id = CharFilter(field_name="session_id", lookup_expr="icontains")
    amount_from = NumberFilter(
        label="Amount from",
        field_name="amount__gte",
        method="filter_amount",
    )
    amount_to = NumberFilter(
        label="Amount to",
        field_name="amount__lte",
        method="filter_amount",
    )
    status = CharFilter(field_name="status", lookup_expr="icontains")
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")

    sort_by = OrderFilter(
        choices=(
            ("session_id", "Session Id ASC"),
            ("-session_id", "Session Id DESC"),
            ("amount", "Amount ASC"),
            ("-amount", "Amount DESC"),
            ("status", "Status ASC"),
            ("-status", "Status DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "session_id": "session_id",
            "-session_id": "-session_id",
            "amount": "amount",
            "-amount": "-amount",
            "status": "status",
            "-status": "-status",
            "created_at": "created_at",
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = Payment
        fields = (
            "session_id",
            "amount_from",
            "amount_to",
            "status",
            "created_at",
            "sort_by",
        )

    def filter_amount(self, queryset, field_name, value):
        lookup_field_name = field_name
        return queryset.filter(**{lookup_field_name: value * 100})

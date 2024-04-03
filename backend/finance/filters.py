from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    DateFilter,
    NumberFilter,
    UUIDFilter,
)
from finance.models import FinanceHistory


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class FinanceHistoryFilter(FilterSet):
    lecturer = UUIDFilter(field_name="lecturer__uuid", lookup_expr="exact")
    account = CharFilter(field_name="account", lookup_expr="contains")
    rate_from = NumberFilter(field_name="rate", lookup_expr="gte")
    rate_to = NumberFilter(field_name="rate", lookup_expr="lte")
    commission_from = CharFilter(field_name="commission", lookup_expr="gte")
    commission_to = CharFilter(field_name="commission", lookup_expr="lte")
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")
    sort_by = OrderFilter(
        choices=(
            ("lecturer", "Lecturer ASC"),
            ("-lecturer", "Lecturer DESC"),
            ("account", "Account ASC"),
            ("-account", "Account DESC"),
            ("rate", "Rate ASC"),
            ("-rate", "Rate DESC"),
            ("commission", "Commission ASC"),
            ("-commission", "Commission DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "lecturer": "lecturer__uuid",
            "-lecturer": "-lecturer__uuid",
            "account": "account",
            "-account": "-account",
            "rate": "rate",
            "-rate": "-rate",
            "commission": "commission",
            "-commission": "-commission",
            "created_at": "created_at",
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = FinanceHistory
        fields = (
            "lecturer",
            "account",
            "rate_from",
            "rate_to",
            "commission_from",
            "commission_to",
            "created_at",
            "sort_by",
        )

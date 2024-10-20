from django_filters import (
    FilterSet,
    CharFilter,
    DateFilter,
    NumberFilter,
)
from finance.models import FinanceHistory
from utils.ordering.ordering import OrderFilter


class FinanceHistoryFilter(FilterSet):
    lecturer_id = NumberFilter(field_name="lecturer__id", lookup_expr="exact")
    account = CharFilter(field_name="account", lookup_expr="contains")
    rate_from = NumberFilter(field_name="rate", lookup_expr="gte")
    rate_to = NumberFilter(field_name="rate", lookup_expr="lte")
    commission_from = CharFilter(field_name="commission", lookup_expr="gte")
    commission_to = CharFilter(field_name="commission", lookup_expr="lte")
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")
    sort_by = OrderFilter(
        choices=(
            ("lecturer_id", "Lecturer Id ASC"),
            ("-lecturer_id", "Lecturer Id DESC"),
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
            "lecturer_id": "lecturer__id",
            "-lecturer_id": "-lecturer__id",
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
            "lecturer_id",
            "account",
            "rate_from",
            "rate_to",
            "commission_from",
            "commission_to",
            "created_at",
            "sort_by",
        )

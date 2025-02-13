from django_filters import (
    FilterSet,
    CharFilter,
    NumberFilter,
    DateFilter,
)
from purchase.models import Purchase, ServicePurchase, Payment
from utils.ordering.ordering import OrderFilter


class PurchaseOrderFilter(OrderFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if "lesson_title" in value or "service_title" in value:
                queryset = queryset.order_by(value.replace("_", "__"))
            else:
                queryset = queryset.order_by(value)

        return queryset


class PurchaseFilter(FilterSet):
    lesson_title = CharFilter(field_name="lesson__title", lookup_expr="icontains")
    price_from = NumberFilter(field_name="price", lookup_expr="gte")
    price_to = NumberFilter(field_name="price", lookup_expr="lte")
    lesson_status = CharFilter(field_name="lesson_status", lookup_expr="exact")
    lecturer_id = NumberFilter(field_name="lecturer_id", lookup_expr="exact")
    review_status = CharFilter(field_name="review_status", lookup_expr="exact")
    review_status_exclude = CharFilter(
        label="Review status exclude",
        field_name="review_status",
        method="filter_review_status_exclude",
    )
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")

    sort_by = PurchaseOrderFilter(
        choices=(
            ("lesson_title", "Lesson Title ASC"),
            ("-lesson_title", "Lesson Title DESC"),
            ("price", "Price ASC"),
            ("-price", "Price DESC"),
            ("lesson_status", "Lesson Status ASC"),
            ("-lesson_status", "Lesson Status DESC"),
            ("review_status", "Review Status ASC"),
            ("-review_status", "Review Status DESC"),
            ("lecturer_id", "Lecturer Id ASC"),
            ("-lecturer_id", "Lecturer Id DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "lesson_title": "lesson__title",
            "-lesson_title": "-lesson__title",
            "price": "price",
            "-price": "-price",
            "lesson_status": "lesson_status",
            "-lesson_status": "-lesson_status",
            "review_status": "review_status",
            "-review_status": "-review_status",
            "lecturer_id": "lecturer_id",
            "-lecturer_id": "-lecturer_id",
            "created_at": "created_at",
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = Purchase
        fields = (
            "lesson_title",
            "price_from",
            "price_to",
            "lesson_status",
            "lecturer_id",
            "review_status",
            "review_status_exclude",
            "created_at",
            "sort_by",
        )

    def filter_review_status_exclude(self, queryset, field_name, value):
        lookup_field_name = field_name
        return queryset.exclude(**{lookup_field_name: value})


class ServicePurchaseFilter(FilterSet):
    service_title = CharFilter(field_name="service__title", lookup_expr="icontains")
    price_from = NumberFilter(field_name="price", lookup_expr="gte")
    price_to = NumberFilter(field_name="price", lookup_expr="lte")
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")

    sort_by = PurchaseOrderFilter(
        choices=(
            ("service_title", "Service Title ASC"),
            ("-service_title", "Service Title DESC"),
            ("price", "Price ASC"),
            ("-price", "Price DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "service_title": "service__title",
            "-service_title": "-service__title",
            "price": "price",
            "-price": "-price",
            "created_at": "created_at",
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = ServicePurchase
        fields = (
            "service_title",
            "price_from",
            "price_to",
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

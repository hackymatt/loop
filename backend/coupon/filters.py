from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    DateFilter,
    NumberFilter,
    BooleanFilter,
)
from coupon.models import Coupon


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class CouponFilter(FilterSet):
    code = CharFilter(field_name="code", lookup_expr="icontains")
    active = BooleanFilter(field_name="active", lookup_expr="exact")
    discount_from = NumberFilter(field_name="discount", lookup_expr="gte")
    discount_to = NumberFilter(field_name="discount", lookup_expr="lte")
    expiration_date_to = DateFilter(field_name="expiration_date", lookup_expr="lte")
    sort_by = OrderFilter(
        choices=(
            ("code", "Code ASC"),
            ("-code", "Code DESC"),
            ("discount", "Discount ASC"),
            ("-discount", "Discount DESC"),
            ("active", "Active ASC"),
            ("-active", "Active DESC"),
            ("expiration_date", "Expiration Date ASC"),
            ("-expiration_date", "Expiration Date DESC"),
        ),
        fields={
            "code": "code",
            "code": "-code",
            "discount": "discount",
            "discount": "-discount",
            "active": "active",
            "active": "-active",
            "expiration_date": "expiration_date",
            "expiration_date": "-expiration_date",
        },
    )

    class Meta:
        model = Coupon
        fields = (
            "code",
            "active",
            "discount_from",
            "discount_to",
            "expiration_date_to",
            "sort_by",
        )

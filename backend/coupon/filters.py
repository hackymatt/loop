from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    DateFilter,
    NumberFilter,
    BooleanFilter,
    UUIDFilter,
)
from coupon.models import Coupon, CouponUser


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if value in ["coupon_code", "-coupon_code"]:
                modified_value = value.replace("_", "__")
                queryset = queryset.order_by(modified_value)
            elif value in ["user_email", "-user_email"]:
                modified_value = value.replace("user_", "user__user__")
                queryset = queryset.order_by(modified_value)
            else:
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


class CouponUserFilter(FilterSet):
    coupon_code = CharFilter(field_name="coupon__code", lookup_expr="icontains")
    user_id = UUIDFilter(field_name="user__uuid", lookup_expr="exact")
    created_at = DateFilter(field_name="created_at", lookup_expr="icontains")

    sort_by = OrderFilter(
        choices=(
            ("coupon_code", "Coupon code ASC"),
            ("-coupon_code", "Coupon code DESC"),
            ("user_email", "User email ASC"),
            ("-user_email", "User email DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "coupon_code": "coupon_code",
            "coupon_code": "-coupon_code",
            "user_email": "user_email",
            "user_email": "-user_email",
            "created_at": "created_at",
            "created_at": "-created_at",
        },
    )

    class Meta:
        model = CouponUser
        fields = (
            "coupon_code",
            "user_id",
            "created_at",
            "sort_by",
        )

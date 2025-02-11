from django_filters import (
    FilterSet,
    NumberFilter,
    CharFilter,
)
from service.models import Service
from utils.ordering.ordering import OrderFilter


class ServiceFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    price_from = NumberFilter(field_name="price", lookup_expr="gte")
    price_to = NumberFilter(field_name="price", lookup_expr="lte")
    active = CharFilter(field_name="active", lookup_expr="exact")
    sort_by = OrderFilter(
        choices=(
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
            ("price", "Price ASC"),
            ("-price", "Price DESC"),
            ("active", "Active ASC"),
            ("-active", "Active DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
            "price": "price",
            "-price": "-price",
            "active": "active",
            "-active": "-active",
        },
    )

    class Meta:
        model = Service
        fields = (
            "title",
            "price_from",
            "price_to",
            "active",
            "sort_by",
        )

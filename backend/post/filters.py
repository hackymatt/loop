from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    BaseInFilter,
)
from post.models import Post


class CharInFilter(BaseInFilter, CharFilter):
    pass


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class PostFilter(FilterSet):
    category = CharFilter(field_name="category__name", lookup_expr="icontains")
    sort_by = OrderFilter(
        choices=(
            ("visits", "Visits ASC"),
            ("-visits", "Visits DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "visits": "visits",
            "-visits": "-visits",
            "created_at": "created_at",
            "created_at": "-created_at",
        },
    )

    class Meta:
        model = Post
        fields = (
            "category",
            "sort_by",
        )

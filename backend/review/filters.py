from django_filters import FilterSet, OrderingFilter, NumberFilter
from review.models import Review


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class ReviewFilter(FilterSet):
    course_id = NumberFilter(field_name="lesson__course__id", lookup_expr="exact")
    lecturer_id = NumberFilter(field_name="lecturer__id", lookup_expr="exact")
    rating = NumberFilter(field_name="rating", lookup_expr="exact")
    rating_from = NumberFilter(field_name="rating", lookup_expr="gte")
    rating_to = NumberFilter(field_name="rating", lookup_expr="lte")
    sort_by = OrderFilter(
        choices=(
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "created_at": "created_at",
            "created_at": "-created_at",
        },
    )

    class Meta:
        model = Review
        fields = (
            "course_id",
            "lecturer_id",
            "rating",
            "rating_from",
            "rating_to",
            "sort_by",
        )

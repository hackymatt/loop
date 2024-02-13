from django_filters import (
    FilterSet,
    OrderingFilter,
    NumberFilter,
)
from lesson.models import (
    LessonPriceHistory,
)


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        return queryset


class LessonPriceHistoryFilter(FilterSet):
    lesson_id = NumberFilter(field_name="lesson__id", lookup_expr="exact")
    sort_by = OrderFilter(
        choices=(
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "created_at": "created_at",
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = LessonPriceHistory
        fields = (
            "lesson_id",
            "sort_by",
        )

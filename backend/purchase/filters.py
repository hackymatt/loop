from django_filters import (
    FilterSet,
    CharFilter,
    NumberFilter,
    DateFilter,
)
from purchase.models import Purchase
from utils.ordering.ordering import OrderFilter


class PurchaseOrderFilter(OrderFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if "lesson_title" in value:
                queryset = queryset.order_by(value.replace("_", "__"))
            else:
                queryset = queryset.order_by(value)

        return queryset


class PurchaseFilter(FilterSet):
    lesson_title = CharFilter(field_name="lesson__title", lookup_expr="icontains")
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

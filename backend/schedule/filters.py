from django_filters import FilterSet, OrderingFilter, NumberFilter
from schedule.models import Schedule


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class ScheduleFilter(FilterSet):
    lesson_id = NumberFilter(field_name="lesson__course__id", lookup_expr="exact")
    lecturer_id = NumberFilter(field_name="lecturer__id", lookup_expr="exact")
    sort_by = OrderFilter(
        choices=(
            ("time", "Time ASC"),
            ("-time", "Time DESC"),
        ),
        fields={
            "time": "time",
            "time": "-time",
        },
    )

    class Meta:
        model = Schedule
        fields = (
            "lesson_id",
            "lecturer_id",
            "sort_by",
        )

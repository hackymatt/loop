from django_filters import FilterSet, OrderingFilter, NumberFilter, UUIDFilter, DateFilter
from schedule.models import Schedule


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class ScheduleFilter(FilterSet):
    lesson_id = NumberFilter(field_name="lesson__id", lookup_expr="exact")
    lecturer_id = UUIDFilter(field_name="lecturer__uuid", lookup_expr="exact")
    time_from = DateFilter(field_name="start_time", lookup_expr="gte")
    time_to = DateFilter(field_name="end_time", lookup_expr="lte")
    sort_by = OrderFilter(
        choices=(
            ("start_time", "Start Time ASC"),
            ("-start_time", "Start Time DESC"),
        ),
        fields={
            "start_time": "start_time",
            "start_time": "-start_time",
        },
    )

    class Meta:
        model = Schedule
        fields = (
            "lesson_id",
            "lecturer_id",
            "time_from",
            "time_to",
            "sort_by",
        )

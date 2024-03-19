from django_filters import (
    FilterSet,
    OrderingFilter,
    NumberFilter,
    UUIDFilter,
    DateFilter,
    BooleanFilter,
    CharFilter,
)
from schedule.models import Schedule


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class ScheduleFilter(FilterSet):
    reserved = BooleanFilter(field_name="lesson", method="filter_reserved")
    lesson_id = NumberFilter(field_name="lesson__id", lookup_expr="exact")
    lecturer_id = UUIDFilter(field_name="lecturer__uuid", lookup_expr="exact")
    time = DateFilter(field_name="start_time", lookup_expr="contains")
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
            "reserved",
            "lesson_id",
            "lecturer_id",
            "time",
            "time_from",
            "time_to",
            "sort_by",
        )

    def filter_reserved(self, queryset, name, value):
        lookup = "__".join([name, "isnull"])
        return queryset.exclude(**{lookup: value})

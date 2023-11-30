from django_filters import FilterSet, OrderingFilter, NumberFilter
from schedule.models import Schedule
from teaching.models import Teaching


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class ScheduleFilter(FilterSet):
    lesson_id = NumberFilter(
        label="Id lekcji równe",
        field_name="lesson",
        method="filter_lesson_id",
    )
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

    def filter_lesson_id(self, queryset, field_name, value):
        lecturers = Teaching.objects.filter(lesson_id=value).values("lecturer")
        return queryset.filter(lecturer__in=lecturers)

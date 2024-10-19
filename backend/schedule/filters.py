from django_filters import (
    FilterSet,
    OrderingFilter,
    NumberFilter,
    DateFilter,
    DateTimeFilter,
    BooleanFilter,
    CharFilter,
)
from schedule.models import Schedule
from lesson.models import Lesson
from django.db.models import OuterRef, Subquery, IntegerField
from django.db.models.expressions import RawSQL
from django.db.models.functions import Cast


def get_free_slots_duration(queryset):
    total_duration = RawSQL(
        """
SELECT EXTRACT(EPOCH FROM (islandenddate - start_time)) / 60 AS difference
 FROM ( SELECT
 id,
 lecturer_id,
 start_time,
 end_time,
 SUM (CASE WHEN Grouping.PreviousEndDate >= start_time THEN 0 ELSE 1 END) OVER (ORDER BY Grouping.RN) AS IslandId
FROM
 (SELECT
  ROW_NUMBER () OVER (ORDER BY lecturer_id, start_time, end_time) AS RN,
  ID,
  lecturer_id,
  start_time,
  end_time,
  MAX(end_time) OVER (PARTITION BY lecturer_id ORDER BY start_time, end_time ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS PreviousEndDate
FROM
  schedule WHERE lesson_id IS NULL) Grouping) AS original LEFT JOIN ( SELECT
  IslandId,
  MAX (end_time) AS IslandEndDate
 FROM
  (SELECT
 *,
 CASE WHEN Grouping.PreviousEndDate >= start_time THEN 0 ELSE 1 END AS IslandStartInd,
 SUM (CASE WHEN Grouping.PreviousEndDate >= start_time THEN 0 ELSE 1 END) OVER (ORDER BY Grouping.RN) AS IslandId
FROM
 (SELECT
  ROW_NUMBER () OVER (ORDER BY lecturer_id, start_time, end_time) AS RN,
  lecturer_id,
  start_time,
  end_time,
  MAX(end_time) OVER (PARTITION BY lecturer_id ORDER BY start_time, end_time ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS PreviousEndDate
FROM
  schedule WHERE lesson_id IS NULL) Grouping
  ) Islands
 GROUP BY
  lecturer_id,
  IslandId
 ORDER BY
  IslandId) AS islands 
  ON original.IslandId = islands.IslandId
  WHERE id = ("schedule"."id")""",
        (),
    )

    return queryset.annotate(duration=Cast(total_duration, IntegerField()))


def get_reserved_slots_duration(queryset):
    total_duration = Lesson.objects.filter(pk=OuterRef("lesson")).values("duration")

    return queryset.annotate(duration=Cast(Subquery(total_duration), IntegerField()))


def filter_lesson(queryset, field_name, value):
    lookup_field_name = f"{field_name}__isnull"
    lesson_records = queryset.filter(**{field_name: value})
    empty_records = queryset.filter(**{lookup_field_name: True})
    return lesson_records | empty_records


def filter_duration(queryset, field_name, value):
    lookup_field_name = f"{field_name}__gte"
    empty_records = queryset.filter(**{"lesson__isnull": True})
    reserved_records = queryset.filter(**{"lesson__isnull": False})

    empty_records_duration = get_free_slots_duration(empty_records).filter(
        **{lookup_field_name: value}
    )
    reserved_records_duration = get_reserved_slots_duration(reserved_records).filter(
        **{lookup_field_name: value}
    )

    records = empty_records_duration | reserved_records_duration

    return records


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class ScheduleFilter(FilterSet):
    reserved = BooleanFilter(field_name="lesson", method="filter_reserved")
    lesson_id = NumberFilter(
        label="Lesson Id",
        field_name="lesson",
        method="filter_lesson",
    )
    lecturer_id = NumberFilter(field_name="lecturer__id", lookup_expr="exact")
    time = DateFilter(field_name="start_time", lookup_expr="contains")
    time_from = DateTimeFilter(field_name="start_time", lookup_expr="gte")
    time_to = DateFilter(field_name="end_time", lookup_expr="lte")
    duration = NumberFilter(
        label="Lesson duration",
        field_name="duration",
        method="filter_duration",
    )
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
            "duration",
            "time",
            "time_from",
            "time_to",
            "sort_by",
        )

    def filter_lesson(self, queryset, field_name, value):
        return filter_lesson(queryset=queryset, field_name=field_name, value=value)

    def filter_reserved(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__isnull"
        return queryset.exclude(**{lookup_field_name: value})

    def filter_duration(self, queryset, field_name, value):
        return filter_duration(queryset=queryset, field_name=field_name, value=value)


class ScheduleAvailableDateFilter(FilterSet):
    lesson_id = NumberFilter(
        label="Lesson Id",
        field_name="lesson",
        method="filter_lesson",
    )
    lecturer_id = NumberFilter(field_name="lecturer__id", lookup_expr="exact")
    duration = NumberFilter(
        label="Lesson duration",
        field_name="duration",
        method="filter_duration",
    )
    year_month = CharFilter(field_name="year_month", lookup_expr="exact")

    class Meta:
        model = Schedule
        fields = (
            "lesson_id",
            "lecturer_id",
            "duration",
            "year_month",
        )

    def filter_lesson(self, queryset, field_name, value):
        return filter_lesson(queryset=queryset, field_name=field_name, value=value)

    def filter_duration(self, queryset, field_name, value):
        return filter_duration(queryset=queryset, field_name=field_name, value=value)

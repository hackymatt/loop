from django_filters import (
    FilterSet,
    CharFilter,
    BaseInFilter,
    NumberFilter,
)
from course.models import Course
from utils.ordering.ordering import OrderFilter


class CharInFilter(BaseInFilter, CharFilter):
    pass


class CourseFilter(FilterSet):
    lecturer_in = CharFilter(
        label="Lecturer in",
        field_name="lecturers_ids",
        method="filter_in",
    )
    technology_in = CharFilter(
        label="Technology in",
        field_name="technologies_names",
        method="filter_in",
    )
    level_in = CharInFilter(field_name="level", lookup_expr="in")
    price_from = NumberFilter(field_name="price", lookup_expr="gte")
    price_to = NumberFilter(field_name="price", lookup_expr="lte")
    rating_from = NumberFilter(field_name="rating", lookup_expr="gte")
    duration_from = NumberFilter(field_name="duration", lookup_expr="gte")
    duration_to = NumberFilter(field_name="duration", lookup_expr="lte")
    sort_by = OrderFilter(
        choices=(
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
            ("level", "Level ASC"),
            ("-level", "Level DESC"),
            ("price", "Price ASC"),
            ("-price", "Price DESC"),
            ("duration", "Duration ASC"),
            ("-duration", "Duration DESC"),
            ("rating", "Rating ASC"),
            ("-rating", "Rating DESC"),
            ("students_count", "Students Count ASC"),
            ("-students_count", "Students Count DESC"),
            ("progress", "Progress ASC"),
            ("-progress", "Progress DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
            "level": "level",
            "level": "-level",
            "price": "price",
            "price": "-price",
            "duration": "duration",
            "duration": "-duration",
            "rating": "rating",
            "rating": "-rating",
            "students_count": "students_count",
            "students_count": "-students_count",
            "progress": "progress",
            "progress": "-progress",
        },
    )

    class Meta:
        model = Course
        fields = (
            "lecturer_in",
            "technology_in",
            "level_in",
            "price_from",
            "price_to",
            "rating_from",
            "duration_from",
            "duration_to",
            "active",
            "sort_by",
        )

    def filter_in(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__contains"

        values = value.split(",")

        v_first, *v_rest = values
        return_queryset = queryset.filter(**{lookup_field_name: [v_first]})
        for v in v_rest:
            return_queryset = return_queryset | queryset.filter(
                **{lookup_field_name: [v]}
            )

        return return_queryset

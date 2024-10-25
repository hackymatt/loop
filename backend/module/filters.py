from django_filters import (
    FilterSet,
    CharFilter,
)
from module.models import Module
from utils.ordering.ordering import OrderFilter


class ModuleFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    sort_by = OrderFilter(
        choices=(
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
            ("duration", "Duration ASC"),
            ("-duration", "Duration DESC"),
            ("price", "Price ASC"),
            ("-price", "Price DESC"),
            ("lessons_count", "Lessons Count ASC"),
            ("-lessons_count", "Lessons Count DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
            "duration": "duration",
            "-duration": "-duration",
            "price": "price",
            "-price": "-price",
            "lessons_count": "lessons_count",
            "-lessons_count": "-lessons_count",
        },
    )

    class Meta:
        model = Module
        fields = (
            "title",
            "sort_by",
        )

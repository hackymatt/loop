from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
)
from module.models import Module
from django.db.models import Count


def get_lessons_count(queryset):
    modules = queryset.annotate(lessons_count=Count("lessons"))

    return modules


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if value in ["lessons_count", "-lessons_count"]:
                queryset = get_lessons_count(queryset).order_by(value)
            else:
                queryset = queryset.order_by(value)

        return queryset


class ModuleFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    sort_by = OrderFilter(
        choices=(
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
            ("lessons_count", "Lessons Count ASC"),
            ("-lessons_count", "Lessons Count DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
        },
    )

    class Meta:
        model = Module
        fields = (
            "title",
            "sort_by",
        )

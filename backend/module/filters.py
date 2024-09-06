from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
)
from module.models import Module


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class ModuleFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    sort_by = OrderFilter(
        choices=(
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
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

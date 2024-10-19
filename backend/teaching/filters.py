from django_filters import (
    FilterSet,
    OrderingFilter,
    NumberFilter,
    CharFilter,
)
from lesson.models import Lesson
from teaching.models import Teaching


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class ManageTeachingFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    duration_from = NumberFilter(field_name="duration", lookup_expr="gte")
    duration_to = NumberFilter(field_name="duration", lookup_expr="lte")
    price_from = NumberFilter(field_name="price", lookup_expr="gte")
    price_to = NumberFilter(field_name="price", lookup_expr="lte")
    github_url = CharFilter(field_name="github_url", lookup_expr="icontains")
    active = CharFilter(field_name="active", lookup_expr="exact")
    teaching = CharFilter(
        label="Teaching równe",
        field_name="teaching_id",
        method="filter_teaching",
    )
    sort_by = OrderFilter(
        choices=(
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
            ("duration", "Duration ASC"),
            ("-duration", "Duration DESC"),
            ("price", "Price ASC"),
            ("-price", "Price DESC"),
            ("github_url", "Github Url ASC"),
            ("-github_url", "Github Url DESC"),
            ("active", "Active ASC"),
            ("-active", "Active DESC"),
            ("teaching", "Teaching ASC"),
            ("-teaching", "Teaching DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
            "duration": "duration",
            "-duration": "-duration",
            "price": "price",
            "-price": "-price",
            "github_url": "github_url",
            "-github_url": "-github_url",
            "active": "active",
            "-active": "-active",
            "teaching": "is_teaching",
            "-teaching": "-is_teaching",
        },
    )

    class Meta:
        model = Lesson
        fields = (
            "title",
            "duration_from",
            "duration_to",
            "price_from",
            "price_to",
            "github_url",
            "active",
            "sort_by",
        )

    def filter_teaching(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__isnull"
        return queryset.filter(**{lookup_field_name: not bool(value)})


class TeachingFilter(FilterSet):
    lesson_id = NumberFilter(field_name="lesson__id", lookup_expr="exact")

    class Meta:
        model = Teaching
        fields = ("lesson_id",)

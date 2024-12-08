from django_filters import FilterSet, CharFilter, DateFilter, NumberFilter
from tag.models import Tag
from utils.ordering.ordering import OrderFilter


class TagFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")
    post_count_gt = NumberFilter(field_name="post_count", lookup_expr="gt")
    course_count_gt = NumberFilter(field_name="course_count", lookup_expr="gt")
    sort_by = OrderFilter(
        choices=(
            ("name", "Name ASC"),
            ("-name", "Name DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
            ("post_count", "Post count ASC"),
            ("-post_count", "Post count DESC"),
            ("course_count", "Course count ASC"),
            ("-course_count", "Course count DESC"),
        ),
        fields={
            "name": "name",
            "-name": "-name",
            "created_at": "created_at",
            "-created_at": "-created_at",
            "post_count": "post_count",
            "-post_count": "-post_count",
            "course_count": "course_count",
            "-course_count": "-course_count",
        },
    )

    class Meta:
        model = Tag
        fields = (
            "name",
            "created_at",
            "post_count_gt",
            "course_count_gt",
            "sort_by",
        )

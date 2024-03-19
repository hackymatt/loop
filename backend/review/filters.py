from django_filters import FilterSet, OrderingFilter, NumberFilter, UUIDFilter
from review.models import Review
from course.models import Course


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class ReviewFilter(FilterSet):
    course_id = NumberFilter(
        label="Course Id",
        field_name="lesson",
        method="filter_course_id",
    )
    lesson_id = NumberFilter(field_name="lesson__id", lookup_expr="exact")
    lecturer_id = UUIDFilter(field_name="lecturer__uuid", lookup_expr="exact")
    student_id = UUIDFilter(field_name="student__uuid", lookup_expr="exact")
    rating = NumberFilter(field_name="rating", lookup_expr="exact")
    rating_from = NumberFilter(field_name="rating", lookup_expr="gte")
    rating_to = NumberFilter(field_name="rating", lookup_expr="lte")
    sort_by = OrderFilter(
        choices=(
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "created_at": "created_at",
            "created_at": "-created_at",
        },
    )

    class Meta:
        model = Review
        fields = (
            "course_id",
            "lesson_id",
            "lecturer_id",
            "student_id",
            "rating",
            "rating_from",
            "rating_to",
            "sort_by",
        )

    def filter_course_id(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__in"

        lessons = Course.lessons.through.objects.filter(course=value).values(
            "lesson_id"
        )

        return queryset.filter(**{lookup_field_name: lessons})

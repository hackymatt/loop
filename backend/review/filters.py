from django_filters import FilterSet, NumberFilter, UUIDFilter
from django.db.models import Subquery
from review.models import Review
from course.models import Course
from utils.ordering.ordering import OrderFilter


class ReviewFilter(FilterSet):
    course_id = NumberFilter(
        label="Course Id",
        field_name="lesson",
        method="filter_course_id",
    )
    lesson_id = NumberFilter(field_name="lesson__id", lookup_expr="exact")
    lecturer_id = NumberFilter(field_name="lecturer__id", lookup_expr="exact")
    lecturer_uuid = UUIDFilter(
        field_name="lecturer__profile__uuid", lookup_expr="exact"
    )
    student_id = NumberFilter(field_name="student__id", lookup_expr="exact")
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
            "-created_at": "-created_at",
        },
    )

    class Meta:
        model = Review
        fields = (
            "course_id",
            "lesson_id",
            "lecturer_id",
            "lecturer_uuid",
            "student_id",
            "rating",
            "rating_from",
            "rating_to",
            "sort_by",
        )

    def filter_course_id(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__in"
        lessons = Course.objects.filter(id=value).values("modules__lessons__id")
        return queryset.filter(**{lookup_field_name: Subquery(lessons)})

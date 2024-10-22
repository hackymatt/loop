from django_filters import FilterSet, NumberFilter, UUIDFilter
from profile.models import LecturerProfile
from utils.ordering.ordering import OrderFilter


class LecturerFilter(FilterSet):
    id = NumberFilter(field_name="id", lookup_expr="exact")
    uuid = UUIDFilter(field_name="profile__uuid", lookup_expr="exact")
    rating_from = NumberFilter(field_name="rating", lookup_expr="gte")
    sort_by = OrderFilter(
        choices=(
            ("full_name", "Full name ASC"),
            ("-full_name", "Full name DESC"),
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
            ("rating", "Rating ASC"),
            ("-rating", "Rating DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
            "rating": "rating",
            "-rating": "-rating",
        },
    )

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "uuid",
            "rating_from",
            "sort_by",
        )

from django_filters import FilterSet, NumberFilter, UUIDFilter
from profile.models import OtherProfile
from utils.ordering.ordering import OrderFilter


class OtherFilter(FilterSet):
    id = NumberFilter(field_name="id", lookup_expr="exact")
    uuid = UUIDFilter(field_name="profile__uuid", lookup_expr="exact")
    sort_by = OrderFilter(
        choices=(
            ("full_name", "Full name ASC"),
            ("-full_name", "Full name DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
        },
    )

    class Meta:
        model = OtherProfile
        fields = (
            "id",
            "uuid",
            "sort_by",
        )

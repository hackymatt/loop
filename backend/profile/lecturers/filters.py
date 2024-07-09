from django_filters import FilterSet, OrderingFilter, NumberFilter, UUIDFilter
from review.models import Review
from profile.models import LecturerProfile
from django.db.models.functions import Concat
from django.db.models import OuterRef, Subquery, Avg, Value


def get_rating(queryset):
    avg_rating = (
        Review.objects.filter(lecturer=OuterRef("pk"))
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(avg_rating=Avg("rating"))
        .values("avg_rating")
    )
    lecturers = queryset.annotate(rating=Subquery(avg_rating))

    return lecturers


def get_full_name(queryset):
    lecturers = queryset.annotate(
        full_name=Concat(
            "profile__user__first_name", Value(" "), "profile__user__last_name"
        )
    )

    return lecturers


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            if value in ["rating", "-rating"]:
                queryset = get_rating(queryset).order_by(value)
            elif value in ["full_name", "-full_name"]:
                queryset = get_full_name(queryset).order_by(value)
            else:
                queryset = queryset.order_by(value)

        return queryset


class LecturerFilter(FilterSet):
    id = UUIDFilter(field_name="profile__uuid", lookup_expr="exact")
    rating_from = NumberFilter(
        label="Rating powyżej lub równe",
        field_name="rating",
        method="filter_rating_from",
    )
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
            "rating_from",
            "sort_by",
        )

    def filter_rating_from(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__gte"
        return get_rating(queryset).filter(**{lookup_field_name: value})

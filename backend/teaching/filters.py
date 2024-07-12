from django_filters import (
    FilterSet,
    OrderingFilter,
    NumberFilter,
    CharFilter,
)
from lesson.models import Lesson
from profile.models import Profile
from teaching.models import Teaching
from django.db.models import OuterRef, Subquery, Exists, Case, When, Value


def get_teaching(self, queryset):
    user = self.request.user
    lecturer = Profile.objects.get(user=user)
    teaching = Teaching.objects.filter(
        lecturer__profile=lecturer, lesson=OuterRef("pk")
    )

    lessons = queryset.annotate(teaching_exists=Subquery(Exists(teaching))).annotate(
        is_teaching=Case(
            When(
                teaching_exists=1,
                then=Value("True"),
            ),
            default=Value("False"),
        )
    )

    return lessons


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
        field_name="is_teaching",
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
        lookup_field_name = field_name
        return get_teaching(self, queryset).filter(**{lookup_field_name: value})


class TeachingFilter(FilterSet):
    lesson_id = NumberFilter(field_name="lesson__id", lookup_expr="exact")

    class Meta:
        model = Teaching
        fields = ("lesson_id",)

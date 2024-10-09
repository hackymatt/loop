from django_filters import (
    FilterSet,
    OrderingFilter,
    CharFilter,
    NumberFilter,
    DateFilter,
)
from post.models import Post, PostCategory
from django.db.models import OuterRef, Subquery, Value, Count, FloatField
from django.db.models.functions import Coalesce


class OrderFilter(OrderingFilter):
    def filter(self, queryset, values):
        if values is None:
            return super().filter(queryset, values)

        for value in values:
            queryset = queryset.order_by(value)

        return queryset


class PostFilter(FilterSet):
    category = CharFilter(field_name="category__name", lookup_expr="icontains")
    sort_by = OrderFilter(
        choices=(
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
            ("active", "Active ASC"),
            ("-active", "Active DESC"),
            ("visits", "Visits ASC"),
            ("-visits", "Visits DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
            "active": "active",
            "-active": "-active",
            "visits": "visits",
            "-visits": "-visits",
            "created_at": "created_at",
            "created_at": "-created_at",
        },
    )

    class Meta:
        model = Post
        fields = (
            "category",
            "active",
            "sort_by",
        )


def get_posts_count(queryset):
    total_posts_count = (
        Post.objects.filter(category__id=OuterRef("pk"))
        .annotate(dummy_group_by=Value(1))
        .values("dummy_group_by")
        .order_by("dummy_group_by")
        .annotate(total_posts_count=Count("id"))
        .values("total_posts_count")
    )
    post_categories = queryset.annotate(
        posts_count=Coalesce(
            Subquery(total_posts_count), Value(0), output_field=FloatField()
        )
    )

    return post_categories


class PostCategoryFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    posts_count_from = NumberFilter(
        label="Liczba artykułów większa lub równa",
        field_name="posts_count",
        method="filter_posts_count_from",
    )
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")
    sort_by = OrderFilter(
        choices=(
            ("name", "Name ASC"),
            ("-name", "Name DESC"),
            ("created_at", "Created At ASC"),
            ("-created_at", "Created At DESC"),
            ("posts_count", "Posts Count ASC"),
            ("-posts_count", "Posts Count DESC"),
        ),
        fields={
            "name": "name",
            "-name": "-name",
            "created_at": "created_at",
            "-created_at": "-created_at",
            "posts_count": "posts_count",
            "-posts_count": "-posts_count",
        },
    )

    class Meta:
        model = PostCategory
        fields = (
            "name",
            "created_at",
            "sort_by",
        )

    def filter_posts_count_from(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__gte"
        return get_posts_count(queryset).filter(**{lookup_field_name: value})

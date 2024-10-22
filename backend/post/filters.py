from django_filters import (
    FilterSet,
    CharFilter,
    NumberFilter,
    DateFilter,
)
from post.models import Post, PostCategory
from utils.ordering.ordering import OrderFilter


class PostFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    category = CharFilter(field_name="category__name", lookup_expr="icontains")
    created_at = DateFilter(field_name="created_at", lookup_expr="contains")
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
            "title",
            "category",
            "created_at",
            "active",
            "sort_by",
        )


class PostCategoryFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    posts_count_from = NumberFilter(field_name="posts_count", lookup_expr="gte")
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

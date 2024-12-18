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
    tags_in = CharFilter(
        label="Tags in",
        field_name="tags_names",
        method="filter_in",
    )
    publication_date = DateFilter(field_name="publication_date", lookup_expr="contains")
    sort_by = OrderFilter(
        choices=(
            ("title", "Title ASC"),
            ("-title", "Title DESC"),
            ("active", "Active ASC"),
            ("-active", "Active DESC"),
            ("visits", "Visits ASC"),
            ("-visits", "Visits DESC"),
            ("publication_date", "Publication date ASC"),
            ("-publication_date", "Publication date DESC"),
        ),
        fields={
            "title": "title",
            "-title": "-title",
            "active": "active",
            "-active": "-active",
            "visits": "visits",
            "-visits": "-visits",
            "publication_date": "publication_date",
            "publication_date": "-publication_date",
        },
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "category",
            "tags_in",
            "publication_date",
            "active",
            "sort_by",
        )

    def filter_in(self, queryset, field_name, value):
        lookup_field_name = f"{field_name}__contains"

        values = value.split(",")

        v_first, *v_rest = values
        return_queryset = queryset.filter(**{lookup_field_name: [v_first]})
        for v in v_rest:
            return_queryset = return_queryset | queryset.filter(
                **{lookup_field_name: [v]}
            )

        return return_queryset


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

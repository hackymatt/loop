from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from post.serializers import (
    PostListSerializer,
    PostGetSerializer,
    PostSerializer,
    PostCategorySerializer,
)
from post.filters import PostFilter, PostCategoryFilter
from post.models import Post, PostCategory
from profile.models import LecturerProfile
from django.db.models import Prefetch


class PostViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = (
        Post.objects.prefetch_related(
            Prefetch("authors", queryset=LecturerProfile.objects.add_full_name())
        )
        .add_duration()
        .add_previous_post()
        .add_next_post()
        .all()
        .order_by("id")
    )
    serializer_class = PostSerializer
    filterset_class = PostFilter
    search_fields = [
        "title",
        "description",
        "content",
        "category__name",
    ]
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == "list":
            queryset = self.queryset
            user = self.request.user

            if user.is_superuser:
                return queryset.distinct()

            active = self.request.query_params.get("active", None)
            if not active:
                return queryset.filter(active=True).all().distinct()

            return queryset.distinct()

        return self.queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        elif self.action == "retrieve":
            return PostGetSerializer
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        post = super().get_object()

        user = self.request.user
        if user.is_superuser:
            return super().retrieve(request, *args, **kwargs)

        if not post.active:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "Nie znaleziono."},
            )

        post.visits = post.visits + 1
        post.save()

        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = super().get_object()

        if post.active:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "Artykuł jest aktywny."},
            )

        return super().destroy(request, *args, **kwargs)


class PostCategoryViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = PostCategory.objects.add_post_count().all().order_by("id")
    serializer_class = PostCategorySerializer
    permission_classes = [AllowAny]
    filterset_class = PostCategoryFilter

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

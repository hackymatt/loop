from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from course.serializers import (
    CourseListSerializer,
    CourseGetSerializer,
    CourseSerializer,
    BestCourseSerializer,
)
from course.filters import (
    CourseFilter,
    get_rating,
)
from course.models import (
    Course,
)
from random import sample


class CourseViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter
    search_fields = [
        "title",
        "description",
        "modules__lessons__title",
        "modules__lessons__description",
    ]
    permission_classes = [AllowAny]

    def get_permissions(self):
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "destroy"
        ):
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == "list":
            user = self.request.user
            if user.is_superuser:
                return self.queryset.distinct()

            active = self.request.query_params.get("active", None)
            if not active:
                return self.queryset.filter(active=True).all().distinct()

            return self.queryset.distinct()

        return self.queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        elif self.action == "retrieve":
            return CourseGetSerializer
        else:
            return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        course = super().get_object()

        user = self.request.user
        if user.is_superuser:
            return super().retrieve(request, *args, **kwargs)

        if not course.active:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "Nie znaleziono."},
            )

        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        course = super().get_object()

        if course.active:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "Kurs jest aktywny."},
            )

        return super().destroy(request, *args, **kwargs)


class BestCourseViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Course.objects.all()
    serializer_class = BestCourseSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = get_rating(queryset=queryset).filter(rating__gte=4)

        ids = queryset.values_list("id", flat=True)
        random_ids = sample(list(ids), min(len(ids), 10))
        return queryset.filter(id__in=random_ids)

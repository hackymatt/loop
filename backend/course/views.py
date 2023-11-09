from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from utils.filtering.backends import ComplexFilterBackend
from course.serializers import (
    CourseListSerializer,
    CourseSerializer,
    TechnologySerializer,
)
from course.filters import CourseFilter
from course.models import Course, Technology
from profile.models import Profile


class TechnologyViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer


class CourseViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (
        ComplexFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = CourseFilter
    search_fields = [
        "title",
        "description",
    ]

    def get_queryset(self):
        if self.action == "list":
            active = self.request.query_params.get("active", None)
            if not active:
                return self.queryset.filter(active=True).all()

            return self.queryset

        return self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Użytkownik niezalogowany."},
            )

        profile = Profile.objects.get(user=user)
        if not profile.user_type == "A":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Brak dostępu."},
            )

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Użytkownik niezalogowany."},
            )

        profile = Profile.objects.get(user=user)
        if not profile.user_type == "A":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Brak dostępu."},
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Użytkownik niezalogowany."},
            )

        profile = Profile.objects.get(user=user)
        if not profile.user_type == "A":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Brak dostępu."},
            )

        if self.get_object().active:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"course": "Kurs jest aktywny."},
            )

        return super().destroy(request, *args, **kwargs)

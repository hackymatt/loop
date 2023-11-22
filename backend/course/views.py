from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from course.serializers import (
    CourseListSerializer,
    CourseGetSerializer,
    CourseSerializer,
    TechnologyListSerializer,
    CoursePriceHistorySerializer,
    LessonPriceHistorySerializer,
)
from course.filters import (
    CourseFilter,
    CoursePriceHistoryFilter,
    LessonPriceHistoryFilter,
    get_rating,
)
from course.models import Course, Technology, CoursePriceHistory, LessonPriceHistory
from profile.models import Profile
from random import sample


class TechnologyViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Technology.objects.all()
    serializer_class = TechnologyListSerializer


class CourseViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put"]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter
    search_fields = [
        "title",
        "description",
        "lessons__title",
        "lessons__description",
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
        elif self.action == "retrieve":
            return CourseGetSerializer
        else:
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


class BestCourseViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = get_rating(queryset=queryset).filter(rating__gte=4)

        ids = queryset.values_list("id", flat=True)
        random_ids = sample(list(ids), min(len(ids), 10))
        return queryset.filter(id__in=random_ids)


class CoursePriceHistoryViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = CoursePriceHistory.objects.all()
    serializer_class = CoursePriceHistorySerializer
    filterset_class = CoursePriceHistoryFilter

    def list(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course-price-history": "Użytkownik niezalogowany."},
            )

        profile = Profile.objects.get(user=user)
        if not profile.user_type == "A":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course-price-history": "Brak dostępu."},
            )

        return super().list(request, *args, **kwargs)


class LessonPriceHistoryViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = LessonPriceHistory.objects.all()
    serializer_class = LessonPriceHistorySerializer
    filterset_class = LessonPriceHistoryFilter

    def list(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course-price-history": "Użytkownik niezalogowany."},
            )

        profile = Profile.objects.get(user=user)
        if not profile.user_type == "A":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course-price-history": "Brak dostępu."},
            )

        return super().list(request, *args, **kwargs)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from course.serializers import (
    CourseListSerializer,
    CourseGetSerializer,
    CourseSerializer,
    BestCourseSerializer,
    LessonDetailsSerializer,
    TechnologyListSerializer,
    CoursePriceHistorySerializer,
    LessonPriceHistorySerializer,
)
from course.filters import (
    CourseFilter,
    CoursePriceHistoryFilter,
    LessonPriceHistoryFilter,
    TechnologyFilter,
    get_rating,
)
from course.models import (
    Course,
    Lesson,
    Technology,
    CoursePriceHistory,
    LessonPriceHistory,
)
from random import sample


class TechnologyViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Technology.objects.all()
    serializer_class = TechnologyListSerializer
    filterset_class = TechnologyFilter


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
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == "create" or self.action == "update":
            permission_classes = [IsAuthenticated & IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.action == "list":
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


class LessonViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Lesson.objects.all()
    serializer_class = LessonDetailsSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated & IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class CoursePriceHistoryViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = CoursePriceHistory.objects.all()
    serializer_class = CoursePriceHistorySerializer
    filterset_class = CoursePriceHistoryFilter
    permission_classes = [IsAuthenticated & IsAdminUser]


class LessonPriceHistoryViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = LessonPriceHistory.objects.all()
    serializer_class = LessonPriceHistorySerializer
    filterset_class = LessonPriceHistoryFilter
    permission_classes = [IsAuthenticated & IsAdminUser]

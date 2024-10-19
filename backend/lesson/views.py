from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from utils.permissions.permissions import IsStudent
from lesson.serializers import (
    LessonGetSerializer,
    LessonSerializer,
    LessonPriceHistorySerializer,
)
from lesson.filters import (
    LessonPriceHistoryFilter,
    LessonFilter,
)
from lesson.models import (
    Lesson,
    LessonPriceHistory,
)


class LessonViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put"]
    queryset = (
        Lesson.objects.prefetch_related("technologies")
        .all()
        .add_lecturers()
        .add_students_count()
        .add_rating()
        .add_rating_count()
        .order_by("id")
    )
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    filterset_class = LessonFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LessonGetSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated, ~IsStudent]
        elif self.action in ["create", "update"]:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class LessonPriceHistoryViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = LessonPriceHistory.objects.all().order_by("id")
    serializer_class = LessonPriceHistorySerializer
    filterset_class = LessonPriceHistoryFilter
    permission_classes = [IsAuthenticated, IsAdminUser]

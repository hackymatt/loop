from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from utils.permissions.permissions import IsStudent
from lesson.serializers import (
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
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    filterset_class = LessonFilter

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAuthenticated & ~IsStudent]
        elif self.action == "create" or self.action == "update":
            permission_classes = [IsAuthenticated & IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class LessonPriceHistoryViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = LessonPriceHistory.objects.all()
    serializer_class = LessonPriceHistorySerializer
    filterset_class = LessonPriceHistoryFilter
    permission_classes = [IsAuthenticated & IsAdminUser]

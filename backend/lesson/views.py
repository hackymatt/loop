from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from lesson.serializers import (
    LessonAdminSerializer,
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
        .add_lecturers_ids()
        .add_students_count()
        .add_rating()
        .add_rating_count()
        .order_by("id")
    )
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    filterset_class = LessonFilter

    def get_serializer_class(self):
        if self.action in ["list"]:
            return LessonAdminSerializer
        elif self.action in ["retrieve"]:
            if self.request.user.is_staff:
                return LessonAdminSerializer
            return LessonGetSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ["list", "create", "update"]:
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

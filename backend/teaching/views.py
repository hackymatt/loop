from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.permissions.permissions import IsLecturer
from teaching.serializers import (
    ManageTeachingSerializer,
    ManageTeachingGetSerializer,
    TeachingSerializer,
)
from teaching.filters import ManageTeachingFilter, get_teaching, TeachingFilter
from lesson.models import Lesson
from teaching.models import Teaching
from django.db.models import Q


class ManageTeachingViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Lesson.objects.all().order_by("id")
    serializer_class = ManageTeachingGetSerializer
    filterset_class = ManageTeachingFilter
    permission_classes = [IsAuthenticated, IsLecturer]

    def get_queryset(self):
        if (
            self.action == "retrieve"
            or self.action == "create"
            or self.action == "destroy"
        ):
            self.filterset_class = None
            return Teaching.objects.all()
        else:
            return get_teaching(self, self.queryset)

    def get_serializer_class(self):
        if (
            self.action == "retrieve"
            or self.action == "create"
            or self.action == "destroy"
        ):
            return ManageTeachingSerializer
        else:
            return self.serializer_class


class TeachingViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Teaching.objects.exclude(
        Q(lecturer__title__isnull=True) | Q(lecturer__description__isnull=True)
    ).order_by("id")
    serializer_class = TeachingSerializer
    filterset_class = TeachingFilter
    permission_classes = [AllowAny]

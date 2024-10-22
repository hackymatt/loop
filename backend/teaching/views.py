from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.permissions.permissions import IsLecturer
from teaching.serializers import (
    ManageTeachingSerializer,
    ManageTeachingGetSerializer,
    TeachingSerializer,
)
from teaching.filters import ManageTeachingFilter, TeachingFilter
from lesson.models import Lesson
from teaching.models import Teaching
from django.db.models import Prefetch
from profile.models import LecturerProfile


class ManageTeachingViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Lesson.objects.all().order_by("id")
    serializer_class = ManageTeachingGetSerializer
    filterset_class = ManageTeachingFilter
    permission_classes = [IsAuthenticated, IsLecturer]

    def get_queryset(self):
        if self.action in ["retrieve", "create", "destroy"]:
            self.filterset_class = None
            return Teaching.objects.all().order_by("id")
        return self.queryset.add_teaching_id(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["retrieve", "create", "destroy"]:
            return ManageTeachingSerializer
        return self.serializer_class


class TeachingViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Teaching.objects.prefetch_related(
        Prefetch(
            "lecturer",
            queryset=LecturerProfile.objects.add_profile_ready().filter(
                profile_ready=True
            ),
        )
    ).order_by("id")
    serializer_class = TeachingSerializer
    filterset_class = TeachingFilter
    permission_classes = [AllowAny]

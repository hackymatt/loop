from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from utils.permissions.permissions import IsLecturer
from teaching.serializers import TeachingSerializer, TeachingGetSerializer
from teaching.filters import TeachingFilter, get_teaching
from lesson.models import Lesson
from teaching.models import Teaching


class TeachingViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Lesson.objects.all()
    serializer_class = TeachingGetSerializer
    filterset_class = TeachingFilter
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
            return TeachingSerializer
        else:
            return self.serializer_class

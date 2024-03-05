from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from utils.permissions.permissions import IsLecturer
from teaching.serializers import TeachingSerializer, TeachingGetSerializer
from lesson.models import Lesson
from profile.models import Profile
from teaching.models import Teaching


class TeachingViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Lesson.objects.all()
    serializer_class = TeachingGetSerializer
    permission_classes = [IsAuthenticated, IsLecturer]

    def get_queryset(self):
        if (
            self.action == "retrieve"
            or self.action == "create"
            or self.action == "destroy"
        ):
            return Teaching.objects.all()
        else:
            return self.queryset

    def get_serializer_class(self):
        if (
            self.action == "retrieve"
            or self.action == "create"
            or self.action == "destroy"
        ):
            return TeachingSerializer
        else:
            return self.serializer_class

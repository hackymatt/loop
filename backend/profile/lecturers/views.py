from rest_framework.viewsets import ModelViewSet
from profile.lecturers.serializers import (
    LecturerSerializer,
)
from profile.models import Profile


class LecturerViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Profile.objects.all()
    serializer_class = LecturerSerializer

    def get_queryset(self):
        return self.queryset.filter(user_type="W").all()

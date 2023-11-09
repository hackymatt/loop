from rest_framework.viewsets import ModelViewSet
from profile.lecturers.serializers import (
    LecturerSerializer,
)
from profile.models import Profile


class LecturerViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Profile.objects.filter(user_type="W").all()
    serializer_class = LecturerSerializer

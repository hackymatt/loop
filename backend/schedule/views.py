from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from utils.permissions.permissions import IsLecturer
from schedule.serializers import ManageScheduleSerializer, ManageScheduleGetSerializer, ScheduleSerializer
from schedule.filters import ScheduleFilter
from schedule.models import Schedule
from profile.models import Profile


class ManageScheduleViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Schedule.objects.all()
    serializer_class = ManageScheduleSerializer
    filterset_class = ScheduleFilter
    permission_classes = [IsAuthenticated, IsLecturer]

    def get_serializer_class(self):
        if self.action == "list":
            return ManageScheduleGetSerializer
        else:
            return self.serializer_class

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        lecturer = Profile.objects.get(user=user)
        return self.queryset.filter(lecturer=lecturer)


class ScheduleViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filterset_class = ScheduleFilter
    permission_classes = [AllowAny]
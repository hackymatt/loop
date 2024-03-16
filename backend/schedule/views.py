from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from utils.permissions.permissions import IsLecturer
from schedule.serializers import ScheduleSerializer, ScheduleGetSerializer
from schedule.filters import ScheduleFilter
from schedule.models import Schedule
from profile.models import Profile


class ScheduleViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filterset_class = ScheduleFilter
    permission_classes = [IsAuthenticated, IsLecturer]

    def get_serializer_class(self):
        if self.action == "list":
            return ScheduleGetSerializer
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

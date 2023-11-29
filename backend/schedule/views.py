from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.permissions.permissions import IsStudent
from schedule.serializers import ScheduleSerializer, ScheduleGetSerializer
from schedule.filters import ScheduleFilter
from schedule.models import Schedule
from profile.models import Profile


class ScheduleViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleGetSerializer
    filterset_class = ScheduleFilter
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated & ~IsStudent]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        profile = Profile.objects.get(user=user)

        data["lecturer"] = profile.id
        serializer = ScheduleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        records = serializer.create(serializer.data)

        return Response(
            status=status.HTTP_201_CREATED,
            data=ScheduleGetSerializer(records, many=True).data,
        )

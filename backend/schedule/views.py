from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from schedule.serializers import (
    ScheduleSerializer,
    ScheduleGetSerializer
)
from schedule.filters import ScheduleFilter
from schedule.models import Schedule
from profile.models import Profile


class ScheduleViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filterset_class = ScheduleFilter

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return ScheduleGetSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"schedule": "Użytkownik niezalogowany."},
            )

        profile = Profile.objects.get(user=user)
        if profile.user_type == "S":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"schedule": "Brak dostępu."},
            )

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"schedule": "Użytkownik niezalogowany."},
            )

        profile = Profile.objects.get(user=user)
        if profile.user_type == "S":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"schedule": "Brak dostępu."},
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"schedule": "Użytkownik niezalogowany."},
            )

        profile = Profile.objects.get(user=user)
        if profile.user_type == "S":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"schedule": "Brak dostępu."},
            )

        return super().destroy(request, *args, **kwargs)

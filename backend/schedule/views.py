from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from schedule.serializers import ScheduleSerializer, ScheduleGetSerializer
from schedule.filters import ScheduleFilter
from schedule.models import Schedule
from profile.models import Profile


class ScheduleViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleGetSerializer
    filterset_class = ScheduleFilter

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data

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

        data["lecturer"] = profile.id
        serializer = ScheduleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        records = serializer.create(serializer.data)

        return Response(
            status=status.HTTP_201_CREATED,
            data=ScheduleGetSerializer(records, many=True).data,
        )

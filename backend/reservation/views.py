from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reservation.serializers import ReservationSerializer
from reservation.models import Reservation
from schedule.models import Schedule
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from config_global import CANCELLATION_TIME, LESSON_DURATION_MULTIPLIER


class ReservationViewSet(ModelViewSet):
    http_method_names = ["post", "delete"]
    queryset = Reservation.objects.all().order_by("id")
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(student__profile__user=user)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user

        reservation = super().get_object()
        schedule = reservation.schedule

        if (schedule.start_time - make_aware(datetime.now())) < timedelta(
            hours=CANCELLATION_TIME
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "Nie można odwołać rezerwacji."},
            )

        other_reservations = (
            Reservation.objects.filter(schedule=schedule)
            .exclude(student__profile__user=user)
            .all()
        )

        if other_reservations.count() == 0:
            duration = (schedule.end_time - schedule.start_time).total_seconds() / 60
            timeslots_count = int(duration / LESSON_DURATION_MULTIPLIER)

            if timeslots_count == 1:
                schedule.lesson = None
                schedule.save()
                deletion = super().destroy(request, *args, **kwargs)
            else:
                lecturer = schedule.lecturer
                start_time = schedule.start_time
                for i in range(timeslots_count):
                    st = start_time + timedelta(minutes=30 * i)
                    et = st + timedelta(minutes=30)
                    Schedule.objects.create(
                        lecturer=lecturer, start_time=st, end_time=et
                    )
                deletion = super().destroy(request, *args, **kwargs)
                schedule.delete()
        else:
            deletion = super().destroy(request, *args, **kwargs)

        return deletion

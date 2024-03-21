from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from reservation.serializers import (
    ReservationSerializer,
    ReservationGetSerializer,
)
from reservation.models import Reservation
from profile.models import Profile
from schedule.models import Schedule
from datetime import timedelta


MIN_LESSON_DURATION_MINS = 30


class ReservationViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return ReservationGetSerializer
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        student = Profile.objects.get(user=user)
        return self.queryset.filter(student=student)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        student = Profile.objects.get(user=user)

        reservation = super().get_object()
        schedule = reservation.schedule

        other_reservations = (
            Reservation.objects.filter(schedule=schedule).exclude(student=student).all()
        )

        if other_reservations.count() == 0:
            duration = (schedule.end_time - schedule.start_time).total_seconds() / 60
            timeslots_count = int(duration / MIN_LESSON_DURATION_MINS)

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

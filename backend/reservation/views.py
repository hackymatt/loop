from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reservation.serializers import (
    ReservationSerializer,
    ReservationGetSerializer,
)
from reservation.models import Reservation
from profile.models import Profile
from schedule.models import Schedule
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from mailer.mailer import Mailer


MIN_LESSON_DURATION_MINS = 30
CANCELLATION_TIME = 24


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

        if (schedule.start_time - make_aware(datetime.now())) < timedelta(
            hours=CANCELLATION_TIME
        ):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "Nie można odwołać rezerwacji."},
            )

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

        mailer = Mailer()

        # notify student
        data = {
            **{
                "lesson_title": reservation.lesson.title,
                "lecturer_full_name": f"{schedule.lecturer.user.first_name} {schedule.lecturer.user.last_name}",
            }
        }
        mailer.send(
            email_template="remove_reservation.html",
            to=[student.user.email],
            subject=f"Odwołanie rezerwacji na lekcję {reservation.lesson.title}.",
            data=data,
        )

        # notify lecturer
        data = {
            **{
                "lesson_title": reservation.lesson.title,
            }
        }
        if other_reservations.count() == 0:
            mailer.send(
                email_template="unreserve_timeslot.html",
                to=[schedule.lecturer.user.email],
                subject="Odwołanie rezerwacji terminu.",
                data=data,
            )

        return deletion

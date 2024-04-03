from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from utils.permissions.permissions import IsLecturer
from schedule.serializers import (
    ManageScheduleSerializer,
    ManageScheduleGetSerializer,
    ScheduleSerializer,
)
from schedule.filters import ScheduleFilter
from schedule.models import Schedule
from profile.models import Profile
from reservation.models import Reservation
from pytz import timezone, utc
from mailer.mailer import Mailer


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

    def destroy(self, request, *args, **kwargs):
        schedule = super().get_object()
        lesson = schedule.lesson
        emails = [
            reservation.student.user.email
            for reservation in Reservation.objects.filter(schedule=schedule).all()
        ]

        deletion = super().destroy(request, *args, **kwargs)

        if lesson is not None:
            mailer = Mailer()
            # notify students
            data = {
                **{
                    "lesson_title": lesson.title,
                    "lecturer_full_name": f"{schedule.lecturer.user.first_name} {schedule.lecturer.user.last_name}",
                    "lesson_start_time": schedule.start_time.replace(tzinfo=utc)
                    .astimezone(timezone("Europe/Warsaw"))
                    .strftime("%d-%m-%Y %H:%M"),
                }
            }
            for email in emails:
                mailer.send(
                    email_template="lesson_cancel.html",
                    to=[email],
                    subject="Twoja lekcja została odwołana.",
                    data=data,
                )

        return deletion


class ScheduleViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filterset_class = ScheduleFilter
    permission_classes = [AllowAny]
